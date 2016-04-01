import requests, json
import time
import sys

x_wait = 30

search_token = str(input('Search token: ')).strip()
token = str(input('Access token from FB: ')).strip()

def get_response(*args, **kwargs):

    # Reason for delay: https://www.facebook.com/help/www/116393198446749
    time.sleep(2)
    r = requests.get(*args, **kwargs)

    if r.status_code == 200:
        return r
    else:
        print('Client received HTTP {0} - payload: {1}'.format(str(r.status_code), str(r.content)))
        print('Waiting for {0} minutes and retrying recursively.'.format(str(x_wait)))
        time.sleep(x_wait*60)
        return get_response(*args, **kwargs)

def search():
    global search_token
    params = {'access_token': token,
              'q': search_token,
              'type': 'page',
              }

    r = get_response('https://graph.facebook.com/v2.5/search', params=params)
    response = r.json()

    print('Search result: ')
    print(json.dumps(response, indent=2))

    if input('Do you want to search for more? (y/n): ') == 'y':
        search_token = str(input('Search term: ')).strip().replace(' ', '%2A')
        search()

# Repeat search
search()

page_id = str(input('Input the Page ID you want to use: ')).strip()

print('Getting posts...')

r = get_response('https://graph.facebook.com/v2.5/{0}/posts'.format(str(page_id)), params={'access_token': token})
response = r.json()
posts = response['data']


data = []
i = 0

more_pages = True
while more_pages:
    next_url = response['paging']['next']

    response = get_response(next_url).json()
    posts += response['data']

    for post in posts:
        next_comment_url = 'https://graph.facebook.com/v2.5/{0}/comments'.format(str(post['id']))
        r = get_response(next_comment_url, params={'access_token': token})
        comment_response = r.json()

        comments = comment_response.get('data')

        if comment_response.get('paging'):
            while comment_response['paging'].get('next'):
                next_comment_url = response['paging']['next']
                comments += get_response(next_comment_url).json()['data']

            print('Received {0} comments from post'.format(str(len(comments))))

        # Add comment to the post dict
        post['comments'] = comments

        r = get_response('https://graph.facebook.com/v2.5/{0}/likes'.format(str(post['id'])), params={'access_token': token})
        like_response = r.json()
        likes = like_response.get('data')

        if like_response.get('paging'):
            while like_response['paging'].get('next'):
                next_like_url = response['paging']['next']
                likes += get_response(next_like_url).json()['data']

            print('Received {0} likes from post'.format(str(len(likes))))

        # Do the save thing with comments
        post['likes'] = likes

    data += posts

    if not response.get('paging'):
        more_pages = False
    elif response['paging'].get('next'):
        more_pages = False

    print('Paging {0}'.format(str(i)))
    i += 1

    # Save everything in a temporary file for each pagination
    f = open(str(page_id) + '_temp_pagination_' + str(i) + '.json', 'w')
    f.write(json.dumps(data, indent=2))
    f.close()


# Write it to a file (optionally disable indentation to save space)
f = open('.'.join([str(page_id), 'json']), 'w')
f.write(json.dumps(data, indent=2))
f.close()
