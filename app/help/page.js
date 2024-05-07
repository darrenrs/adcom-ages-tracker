import { PUBLISHER_TITLE_LEGAL } from "@/app/constants";

export default function Help() {
  return (
    <div className="help-root">
      <h1 className="global-title">Mission Tracker</h1>
      <section>
        <h2>What is the Mission Tracker?</h2>
        <p>The Mission Tracker is a helpful tool for the Hyper Hippo mobile idle games AdVenture Communist and AdVenture Ages. It includes an advanced calculator for all missions in both games as well as information about different researchers and heroes.</p>
      </section>
      <section>
        <h2>How does this differ from the original Tracker?</h2>
        <p>The original Tracker was created by Zephyron in May 2019. It was originally intended to be a simple mission list, but as the game's community grew, more features were added. After a few years, the original Tracker did not effectively suit the needs of the community. The new Tracker is designed to function in a more efficient and versatile manner which should serve the community for an indefinite time with minimal maintenance. It utilizes the full-stack PERN model to better streamline communication between the client and server and fixes many bugs and quirks in the original vanilla JS Tracker.</p>
      </section>
      <section>
        <h2>Who maintains the Tracker?</h2>
        <p>My online alias is Enigma. You can reach out to me on Discord as enigma.code or GitHub as darrenrs. I will respond to issues or allegations within a one-week window.</p>
      </section>
      <section>
        <h2>How can I import my data?</h2>
        <p>Inbound users from the original Tracker may import their data into the browser.</p>
      </section>
      <section>
        <h2>What does creating a user account entail?</h2>
        <p>It is strongly recommended to create a user account if you plan on using the Tracker on multiple devices. This will allow you to sync your data on both games between devices via the server. Your user data is securely stored in a password-secured Postgres database masked by CloudFlare DNS.</p>
      </section>
      <section>
        <h2>I have privacy concerns!</h2>
        <p>Privacy is an essential right of all human beings. However, like all websites, there is some extent of data collection. All users who visit this site will have their Internet (IP) address recorded for an indefinite amount of time. Furthermore, creation of a user account implies association of IP address with potentially identifying information. No identifying data are shared with external parties and this site does not collect ad revenue or utilize advertising services. If you do not agree to the scope of data collection, you have the right to not use this site and to not create a user account. If you develop privacy concerns after visiting this site or creating a user account, you have the right to request a full deletion of your data from the server within 90 days of the originating request.</p>
      </section>
      <section>
        <h2>What are the terms of this site?</h2>
        <p>By using this website, you agree to the following terms:</p>
        <ul className="list-disc ml-12">
          <li>You will not attempt to create or otherwise herald a denial-of-service attack against the host server</li>
          <li>You will not attempt to breach the server with malicious intent to steal unauthorized user data or access unauthorized areas</li>
          <li>You will not claim credit for any site features that were not created or contributed to under your identity</li>
          <li>You will not store illegal materials or content such as child pornography, terrorist threats, copyrighted material, etc. in any manner in populated fields</li>
          <li>You will abide to any additional terms that may be posted without notice to this page</li>
        </ul>
        <p>Should you be proven in violation of these terms, your access may be immediately and permanently suspended at the owner's discretion with the potential risk of being elevated to law enforcement if such actions fall under a violation of U.S.C. Title 18.</p>
      </section>
      <section>
        <h2>Does this product imply that I am a Communist?</h2>
        <p>The nature of one of these games being "communist" themed is merely a satirical matter--there is no causal link to AdVenture Communist and/or AdVenture Ages players and support of Marxism or other radical ideologies. My involvement with Hyper Hippo games is rooted in passion for idle games, not politics. As such, there should not be any notion of an endorsement of any specific political and/or economic ideology.</p>
      </section>
      <div className="inset-x-0 top-0 bg-neutral-200 dark:bg-neutral-950 p-2 -m-4 mt-4 border-solid border-t border-t-neutral-400 leading-loose">
        <div>&copy; 2024 Darren R. Skidmore. All rights reserved. This material is not official and is not endorsed by Hyper Hippo. For more information, see <a href="https://hyperhippo.com/fan-content-policy/" className="global-link">Hyper Hippo's Fan Content Policy.</a></div>
        <div>All proprietary materials &copy; 2017-24 {PUBLISHER_TITLE_LEGAL}.</div>
      </div>
    </div>
  );
}
