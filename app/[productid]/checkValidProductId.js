const VALID_PRODUCT_IDS = [
  "adcom",
  "ages"
];

export default function IsValidProductId(productId) {
  return VALID_PRODUCT_IDS.includes(productId);
}