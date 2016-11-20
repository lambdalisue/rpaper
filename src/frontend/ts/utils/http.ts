import 'isomorphic-fetch';
import * as Cookies from 'js-cookie';


export class HTTPError extends Error {
  response: Response;
  constructor(response: Response) {
    super(response.statusText);
    this.response = response;
  }
}

export interface RequestInitWithParams extends RequestInit {
  params?: { [key: string]: string };
}

export function request(url: RequestInfo,
                        init: RequestInitWithParams={}): Promise<Response> {
  // Add GET URL params if necessary
  if (init.params !== undefined) {
    url = `${url}?${buildQueryParam(init.params)}`;
    delete init.params;
  }

  // Add django CSRF token if necessary
  if (!csrfSafeMethod(init.method || 'GET') && init.mode !== 'cors') {
    const csrftoken = Cookies.get('csrftoken');
    init.headers = init.headers || {};
    init.headers['X-CSRFToken'] = csrftoken;
  }

  // TODO: REMOVE IT IN PRODUCTION
  console.debug('http.request', url, init);

  return fetch(url, init).then((response) => {
    if (response.ok) {
      return response;
    }
    throw new HTTPError(response);
  });
}

function csrfSafeMethod(method: string): boolean{
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// http://stackoverflow.com/questions/34692554/url-query-string-in-fetch-api-in-javascript
function buildQueryParam(query: { [key: string]: string }): string {
  return Object.keys(query)
               .map((key) => encodeURIComponent(key) + "=" + encodeURIComponent(query[key]))
               .join("&")
               .replace(/%20/g, "+");
}
