# adapted from iambibhas's Python Imgur image uploader:
# https://gist.github.com/iambibhas/6855102

import json
import sys
from sh import curl

try:
    resp = curl(
        "https://api.imgur.com/3/image",
        H="Authorization: Client-ID ",
        X="POST",
        F='image=@%s' % sys.argv[1]
    )
    objresp = json.loads(resp.stdout)

    if objresp.get('success', False):
        f = open('link.txt', 'w+')
        f.write(objresp['data']['link'])
        f.close()
    else:
        print('Error: ', objresp['data']['error'])
except Exception as e:
    print('Error: ', e)
