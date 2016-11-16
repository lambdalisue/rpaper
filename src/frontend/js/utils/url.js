// http://stackoverflow.com/questions/34692554/url-query-string-in-fetch-api-in-javascript
export function buildQueryParam(query) {
  return Object.keys(query)
               .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(query[key]))
               .join("&")
               .replace(/%20/g, "+");

}
