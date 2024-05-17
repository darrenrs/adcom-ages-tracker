#!/usr/bin/env python3
# This script is invoked by the Node.js runtime and downloads/extracts game assets in the required directory structure.
# UnityPy (https://pypi.org/project/UnityPy/) must be installed on the target Python instance in order to parse Unity AssetBundles.
# Requires valid iOS Game Center ID in ENV file.

import os
import json
import requests
import gzip
import shutil
import argparse
import asyncio
import aiohttp
import UnityPy
import re
from dotenv import load_dotenv

VALID_TITLE_IDS = [
  '6bf5',
  'dc4bb'
]

ADCOM_FUSIONS = [
  'fusfarm',
  'fuspet',
  'fusscience',
  'fusvehicle'
]

# Copy these from evergreen to shared file
SHARED_ICONS = [
  'cards',
  'crit',
  'flag',
  'output',
  'power',
  'price',
  'speed'
]

# Do not copy these
ICON_DO_NOT_COPY = [
  'back-to-evergreen',
  'darkscience-pack-1',
  'darkscience-pack-2',
  'darkscience-pack-3',
  'lte-common',
  'lte-rare',
  'not-available',
  'plus',
  'promote-researcher-arrow',
  'researcherframe-common',
  'researcherframe-rare',
  'science-pack-1',
  'science-pack-2',
  'science-pack-3',
  'science-pack-4',
  'science-pack-5',
  'science-pack-6'
]

HARDCODED_RESOURCE_MAPPINGS = {
  '6bf5': [
    ('time-hack-1', 'timehack_1'),
    ('time-hack-2', 'timehack_4'),
    ('time-hack-3', 'timehack_24'),
    ('time-hack-4', 'timehack_8'),
    ('time-hack-5', 'timehack_12'),
    ('time-hack-6', 'timehack_free')
  ],
  'dc4bb': [
    ('time-hack-1', 'timehack_1'),
    ('time-hack-2', 'timehack_4'),
    ('time-hack-3', 'timehack_8'),
    ('time-hack-4', 'timehack_12'),
    ('time-hack-5', 'timehack_24'),
    ('time-hack-30', 'timehack_free')
  ]
}  # TODO: fill this out

REGEX_RESEARCHER_IMAGE = re.compile('[A-Z]+\d+.png')
REGEX_CAPSULE_IMAGE = re.compile('icon-.*-medium\.png')

def parse_version(version_string):
  return tuple(map(int, version_string.split('.')))

def get_most_recent(path):
  version_files = os.listdir(path)
  versions = sorted((parse_version(file_name) for file_name in version_files), reverse=True)
  
  if versions:
    return '.'.join(map(str, versions[0]))

def get_filename_from_url(url):
  return url.split('/')[-1]

def path_meets_requirements(filename):
  return '.json.gz' in filename and\
    ('Balance' in filename or\
     'Localization.English' in filename or\
     'LteSchedule' in filename)

def convert_ab_to_bal(ab_id):
  hashtable = {
    "fusionarchitecture": "architecture",
    "fusioncareers": "careers",
    "fusioninfrastructure": "infrastructure",
    "fusioninnovation": "innovation",
    "halloween": "monster"
  }
  
  if ab_id in hashtable:
    return hashtable[ab_id]

  return ab_id

async def download_file(session, url, destination):
  async with session.get(url) as response:
    response.raise_for_status()
    
    with open(destination, 'wb') as f:
      while True:
        chunk = await response.content.read(1024)
        if not chunk:
          break
        f.write(chunk)

async def dump_data(title_id, data):
  # Main data (json, txt)
  manifest = f'manifest_{title_id}.json'

  # Create directories
  base_path = os.path.join(os.path.dirname(__file__), '..')
  path_tmp = os.path.join(base_path, 'tmp')
  path_gz = os.path.join(path_tmp, f'{title_id}_gz')
  path = os.path.join(path_tmp, title_id)

  os.makedirs(path_gz, exist_ok=True)
  os.makedirs(path, exist_ok=True)
  
  with open(os.path.join(path_tmp, manifest), 'w') as f:
    json.dump(data, f, indent=2)  # formatting may be helpful for debugging manifest file, which does not need to be minified
  
  requested_files = []

  # Download files
  for k in data:
    if isinstance(data[k], dict):
      for l in data[k]:
        # ignore some files that are not needed, like restricted regions
        if path_meets_requirements(data[k][l]):
          requested_files.append(data[k][l])
    
    elif data[k] is not None and path_meets_requirements(data[k]):
      requested_files.append(data[k])
  
  async with aiohttp.ClientSession() as session:
    tasks = [download_file(session, url, os.path.join(path_gz, url.split('/')[-1])) for url in requested_files]
    for f in tasks:
      await f

  for i in os.listdir(path_gz):
    with gzip.open(os.path.join(path_gz, i), 'rb') as fa:
      if 'Localization' in i:
        output_name = f"{i[:-8]}.txt"  # remove JSON extension from TXT file
      else:
        output_name = i[:-3]
      
      with open(os.path.join(path, output_name), 'wb+') as fb:
        shutil.copyfileobj(fa, fb)

    if 'Localization' not in i:
      # format JSON file
      with open(os.path.join(path, output_name), 'r+') as f:
        preformatted = json.load(f)
        f.seek(0)
        f.truncate()
        json.dump(preformatted, f)
  
  # create "shared" folder
  path_shared = os.path.join(path, 'shared', 'gacha')
  os.makedirs(path_shared, exist_ok=True)

  # Reorganize directory structure
  for i in data["Balance"]:
    balance_id = i.split('-')[0]

    filename_tmp = data["Balance"][i].split('/')[-1].replace('.gz', '')

    path_bal = os.path.join(path, balance_id)
    path_a = os.path.join(path, filename_tmp)

    # this is global configuration and shouldn't be in its own folder
    if balance_id == 'common':
      path_b = os.path.join(path, f"{i}.json")
    else:
      os.makedirs(path_bal, exist_ok=True)
      
      path_researcher = os.path.join(path_bal, 'researcher')
      path_icon = os.path.join(path_bal, 'icon')
      path_iconrank = os.path.join(path_bal, 'rank')

      os.makedirs(path_researcher, exist_ok=True)
      os.makedirs(path_icon, exist_ok=True)

      # rank images only in Com
      if title_id == '6bf5':
        os.makedirs(path_iconrank, exist_ok=True)
      
      path_b = os.path.join(path_bal, f"{i}.json")

    os.rename(path_a, path_b)

  lteschedule_tmp = data["LteScheduleUrl"].split('/')[-1].replace('.gz', '')
  localization_tmp = data["LocalizationConfig"]["English"].split('/')[-1].replace('.json.gz', '.txt')

  os.rename(os.path.join(path, lteschedule_tmp), os.path.join(path, 'schedule.json'))
  os.rename(os.path.join(path, localization_tmp), os.path.join(path, 'localization_en-US.txt'))

  # Unity assetbundles
  path_ab = os.path.join(path_tmp, f"{title_id}_ab")

  os.makedirs(path_ab, exist_ok=True)
  
  ab_manifest_url = f'{data["AssetBundleUrl"]}/ios/{data["ManifestName"]}'

  async with aiohttp.ClientSession() as session:
    await download_file(session, ab_manifest_url, os.path.join(path_tmp, data["ManifestName"]))

  requested_files_ab = []

  uab = UnityPy.load(os.path.join(path_tmp, data["ManifestName"]))
  for obj in uab.objects:
    if obj.type.name == 'AssetBundleManifest':
      for i in obj.read()['AssetBundleNames']:
        ab_url = f'{data["AssetBundleUrl"]}/ios/{i[1]}'
        ab_prefix_id = i[1].split('/')[0].split('_')[0]

        requested_files_ab.append((ab_url, ab_prefix_id))
    
  async with aiohttp.ClientSession() as session:
    tasks = [download_file(session, url, os.path.join(path_ab, f"{prefix_id}_bundle")) for (url, prefix_id) in requested_files_ab]
    for f in tasks:
      await f

  path_ab_tmp_list = [i for i in os.listdir(path_ab) if os.path.isfile(os.path.join(path_ab, i))]

  for i in path_ab_tmp_list:
    path_ab_specific = os.path.join(path_ab, i.replace('_bundle', ''))

    os.makedirs(path_ab_specific, exist_ok=True)

    uab = UnityPy.load(os.path.join(path_ab, i))
    for obj in uab.objects:
      if obj.type.name in ["Texture2D", "Sprite"]:
        data = obj.read()
        
        dest = os.path.join(path_ab_specific, data.name)

        dest, _ = os.path.splitext(dest)
        dest = f"{dest}.png"

        img = data.image
        img.save(dest)

  # Sort out Unity assetbundles using an algorithmic method, but file naming inconsistencies mean that some paths will have to be hardcoded

  # Shared assets
  path_ab_evergreen = os.path.join(path_ab, 'evergreen')
  path_ab_common = os.path.join(path_ab, 'common')
  path_ab_ltehistory = os.path.join(path_ab, 'ltehistory')

  for i in SHARED_ICONS:
    path_origin_ab = os.path.join(path_ab_evergreen, f"{i}.png")
    path_dest = os.path.join(path, 'shared', f"{i}.png")

    with open(path_origin_ab, 'rb') as origin:
      with open(path_dest, 'wb+') as dest:
        shutil.copyfileobj(origin, dest)

  for i in os.listdir(path_ab_common):
    if re.match(REGEX_CAPSULE_IMAGE, i):
      capsule_id = i.split('-')[-2]
      path_origin_ab = os.path.join(path_ab_common, i)
      path_dest = os.path.join(path, 'shared', 'gacha', f"{capsule_id}.png")

      with open(path_origin_ab, 'rb') as origin:
        with open(path_dest, 'wb+') as dest:
          shutil.copyfileobj(origin, dest)
  
  path_upgrade_ab = os.path.join(path_ab_evergreen, 'icon-promote-researcher-arrow.png')
  path_upgrade_ab_dest = os.path.join(path, 'shared', 'upgrade.png')

  with open(path_upgrade_ab, 'rb') as origin:
    with open(path_upgrade_ab_dest, 'wb+') as dest:
      shutil.copyfileobj(origin, dest)
  
  path_upgrade_lte_ab = os.path.join(path_ab_common, 'icon-promote-researcher-arrow-lte.png')
  path_upgrade_lte_ab_dest = os.path.join(path, 'shared', 'upgrade_lte.png')

  with open(path_upgrade_lte_ab, 'rb') as origin:
    with open(path_upgrade_lte_ab_dest, 'wb+') as dest:
      shutil.copyfileobj(origin, dest)

  # Researcher images
  ab_list = os.listdir(path_ab)
  for i in ab_list:
    path_ab_bal = os.path.join(path_ab, i)

    if os.path.isdir(path_ab_bal) and i not in ['common', 'ltehistory', 'fusion']:
      balance_file_list = os.listdir(path_ab_bal)

      for j in balance_file_list:
        path_ab_bal_file = os.path.join(path_ab_bal, j)
        path_dest = os.path.join(path, convert_ab_to_bal(i), 'researcher', j)
        
        if re.match(REGEX_RESEARCHER_IMAGE, j):
          with open(path_ab_bal_file, 'rb') as origin:
            with open(path_dest, 'wb+') as dest:
              shutil.copyfileobj(origin, dest)

  # Resource icons
  for i in ab_list:
    path_ab_bal = os.path.join(path_ab, i)

    if os.path.isdir(path_ab_bal) and i not in ['common', 'ltehistory', 'fusion']:
      balance_file_list = os.listdir(path_ab_bal)

      for j in balance_file_list:
        filename_lower = j.lower()
        path_ab_bal_file = os.path.join(path_ab_bal, j)
        
        if filename_lower[:4] == 'icon':
          predicted_name = filename_lower.replace('icon-', '').replace('icon_', '')
          path_dest = os.path.join(path, convert_ab_to_bal(i), 'icon', predicted_name)

          # event icon; specified with the wrong ID in monster/halloween balance
          if predicted_name == 'multi-industry.png' or predicted_name == 'mainmenu_220px.png':
            path_dest = os.path.join(path, convert_ab_to_bal(i), 'icon.png')
          
          # actual conversion for non-standard names
          for k in HARDCODED_RESOURCE_MAPPINGS[title_id]:
            if predicted_name.replace('.png', '') == k[0]:
              path_dest = os.path.join(path, convert_ab_to_bal(i), 'icon', f"{k[1]}.png")

          # exclude some unneeded assets
          if predicted_name.replace('.png', '') in ICON_DO_NOT_COPY or (title_id == '6bf5' and predicted_name == 'icon-darkscience.png') or 'rank-' in predicted_name:
            continue
          
          with open(path_ab_bal_file, 'rb') as origin:
            with open(path_dest, 'wb+') as dest:
              shutil.copyfileobj(origin, dest)
  
      # must copy darkscience asset from common
      if title_id == '6bf5':
        path_darksci_com_ab = os.path.join(path_ab_common, 'icon-darkscience.png')
        path_dest = os.path.join(path, convert_ab_to_bal(i), 'icon', 'darkscience.png')
            
        with open(path_darksci_com_ab, 'rb') as origin:
          with open(path_dest, 'wb+') as dest:
            shutil.copyfileobj(origin, dest)
    
    elif i == 'fusion':
      path_ab_fusionshared_com = os.path.join(path_ab, 'fusion')
      
      for j in ADCOM_FUSIONS:
        path_fusion_dir = os.path.join(path, j, 'icon')
      
        paths = [
          ('icon-comrade', 'comrade'),
          ('icon-time-hack-1', 'timehack_1'),
          ('icon-time-hack-2', 'timehack_4'),
          ('icon-time-hack-3', 'timehack_24'),
          ('icon-time-hack-4', 'timehack_8'),
          ('icon-time-hack-5', 'timehack_12'),
          ('icon-time-hack-6', 'timehack_free')
        ]

        for k in paths:
          with open(os.path.join(path_ab_fusionshared_com, f"{k[0]}.png"), 'rb') as origin:
            with open(os.path.join(path_fusion_dir, f"{k[1]}.png"), 'wb+') as dest:
              shutil.copyfileobj(origin, dest)
  
  path_evergreen_icon = os.path.join(path, 'evergreen', 'icon.png')
  path_global_icon = os.path.join(path, 'icon.png')
            
  with open(path_evergreen_icon, 'rb') as origin:
    with open(path_global_icon, 'wb+') as dest:
      shutil.copyfileobj(origin, dest)

  # Rank icons (AdCom only)
  if title_id == '6bf5':
    evergreen_file_list = os.listdir(path_ab_evergreen)
    for i in evergreen_file_list:
      if 'icon-rank-' in i:
        rank_num = re.findall(r'\d+', i)[0]

        path_evergreen_rank_ab = os.path.join(path_ab_evergreen, i)
        path_dest = os.path.join(path, 'evergreen', 'rank', f"{rank_num}.png")
            
        with open(path_evergreen_rank_ab, 'rb') as origin:
          with open(path_dest, 'wb+') as dest:
            shutil.copyfileobj(origin, dest)
    
    ltehistory_file_list = os.listdir(path_ab_ltehistory)
    for i in ltehistory_file_list:
      filename_lower = i.lower()

      if 'rank' in filename_lower:
        balance_id = filename_lower[:filename_lower.index('rank')]
        rank_num = re.findall(r'\d+', i)[0]

        # have to propagate it manually for all fusions
        if balance_id == 'fusion':
          for x in ADCOM_FUSIONS:
            path_lte_rank_ab = os.path.join(path_ab_ltehistory, i)
            path_dest = os.path.join(path, x, 'rank', f"{rank_num}.png")
                
            with open(path_lte_rank_ab, 'rb') as origin:
              with open(path_dest, 'wb+') as dest:
                shutil.copyfileobj(origin, dest)
        else:
          path_lte_rank_ab = os.path.join(path_ab_ltehistory, i)
          path_dest = os.path.join(path, balance_id, 'rank', f"{rank_num}.png")
              
          with open(path_lte_rank_ab, 'rb') as origin:
            with open(path_dest, 'wb+') as dest:
              shutil.copyfileobj(origin, dest)

  # Copy tree to public directory
  public_loc = os.path.join(base_path, 'public', 'assets', title_id)
  shutil.copytree(path, public_loc, dirs_exist_ok=True)

  print('The operation completed successfully')

if __name__ == '__main__':
  args = argparse.ArgumentParser()
  args.add_argument('-g', '--game', help='Title ID')
  args.add_argument('-v', '--version', help='Version')
  args_struct = args.parse_args()
    
  if args_struct.game and args_struct.version:
    if args_struct.game not in VALID_TITLE_IDS:
      print('Unknown title ID')
      exit(1)

    load_dotenv(dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env'))
    PLAYER_ID = os.getenv('GC_PLAYER_ID')

    with open('gc-auth-body.json', 'r') as f:
      GC_AUTH_BODY = json.load(f)
      GC_AUTH_BODY["PlayerId"] = PLAYER_ID
      GC_AUTH_BODY["TitleId"] = args_struct.game.upper()
      REQUEST_URL_AUTH = f"https://{args_struct.game}.playfabapi.com/Client/LoginWithGameCenter"

    r = requests.post(REQUEST_URL_AUTH, json=GC_AUTH_BODY).json()
    session_token = r["data"]["SessionTicket"]

    with open('gc-balance-body.json', 'r') as f:
      GC_BAL_BODY = json.load(f)
      GC_BAL_BODY["FunctionParameter"]["DataVersion"] = args_struct.version
      REQUEST_URL_CSCRIPT = f"https://{args_struct.game}.playfabapi.com/Client/ExecuteCloudScript"
    
    r = requests.post(REQUEST_URL_CSCRIPT, json=GC_BAL_BODY, headers={
      'Content-type': 'application/json',
      'X-Authorization': session_token
    }).json()

    try:
      all_data = json.loads(r["data"]["FunctionResult"])
    except:
      print('No data for this version found')
      exit(2)
    

    asyncio.run(dump_data(args_struct.game, all_data))

    # try:
    #   asyncio.run(dump_data(args_struct.game, all_data))
    # except:
    #   print('An error occurred while extracting data')
    #   exit(2)
  
  else:
    print('Missing required parameters')
    exit(1)