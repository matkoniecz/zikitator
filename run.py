import requests
import requests_cache
import zikit_labels
import config
from leaflet import get_before, get_after, get_marker

requests_cache.install_cache(config.get_cache_name())
import re
import json

with open(config.get_token_location()) as f:
    token = f.read()

standard_headers = {'User-Agent': 'github-zikitator/0.0',
                    'Authorization': 'bearer {0}'.format(token)}


class Marker:
    pass


active_markers = []
not_dead_markers = []
succesful_markers = []

def main():
    process('matkoniecz/bicycle_map_of_Krakow', 'OSM',
        state='open',
        inactive=["rendering"], 
        closed=[], 
        active=["missing OSM data", "missing OSM data - bicycle parking"], 
        without_location=[],
        success = []
    )

    process('matkoniecz/krakow', 'ZIKIT',
        state='all',
        inactive=zikit_labels.get_inactive_labels(), 
        closed=zikit_labels.get_closed_labels(), 
        active=zikit_labels.get_activating_labels(), 
        without_location=zikit_labels.get_labels_marking_unlocatable(),
        success = zikit_labels.get_success_labels()
    )



def process(repo, main_name, state, inactive, closed, active, without_location, success):
    active_markers.clear()
    not_dead_markers.clear()
    succesful_markers.clear()
    print(repo)
    page = 1
    while True:
        issues_json = fetch_issues(repo, page, state)
        if len(issues_json) == 0:
            break

        for issue in issues_json:
            #print(issue)
            process_issue(repo, issue, inactive, closed, active, without_location, success)
        page += 1
    name = main_name
    write_markers_to_data_file(name+'.data', active_markers, name)
    print(str(len(active_markers))+ " active markers from Github ("+repo+")")
    write_markers_to_standalone_file(name+'.html', active_markers, name)
    name = main_name + '-all'
    write_markers_to_standalone_file(name+'.html', not_dead_markers, name)
    name = main_name + '-succesful'
    write_markers_to_standalone_file(name+'.html', succesful_markers, name)

def fetch_issues(repo, page, issue_state):
    issues_url = 'https://api.github.com/repos/{0}/issues'.format(repo)
    r = requests.get(issues_url,
                     params={'per_page': '100',
                             'page': str(page),
                             'state': issue_state},
                     headers=standard_headers)
    if r.status_code != 200:
        raise Exception("HTTP status {0} on fetching {1}".format(
            r.status_code,
            issues_url))

    issues_json = r.json()
    return issues_json

def complain_about_issue_with_missing_location(description, label_names):
    print(description)
    for label in label_names:
        print("\t" + label)
    print("\tWithout any given location!")
    print("")

def link_to_lat_lon(link):
    # print("\t" + link)
    lat = None
    lon = None
    for location in re.findall('\d+\.\d+', link):
        if location is not None:
            if lat is None:
                lat = location
            else:
                lon = location
                break
    return lat, lon

def get_text_of_comments(issue):
    comments = ""
    if issue['comments'] > 0:
        comments_request = requests.get(issue['comments_url'], headers=standard_headers)
        for comment in comments_request.json():
            comments += comment['body']
    return comments

def process_issue(repo, issue, inactivating_labels, closing_labels, activating_labels, without_location, success_labels):
    """
    issues_url = 'https://api.github.com/rate_limit'
    r = requests.get(issues_url,
                     headers=standard_headers)
    print()
    print()
    print()
    print(r.json())
    print()
    print()
    print()
    """

    number = issue['number']
    title = issue['title']
    labels = issue['labels']
    body = issue['body']

    description = str(number) + " " + title + " \n" + github_link(repo, number)

    active = True
    not_dead = True
    reactivated = False
    locatable = True
    success = False
    label_names = [label['name'] for label in labels]
    for label in label_names:
        if label in inactivating_labels:
            active = False
        if label in closing_labels:
            not_dead = False
        if label in activating_labels:
            reactivated = True
        if label in success_labels:
            success = True
        if label in without_location:
            locatable = False

    if reactivated:
        not_dead = True
        active = True

    body += get_text_of_comments(issue)
    links = re.findall('openstreetmap.org[^ \n\t]*', body)
    located = False
    for link in links:
        lat, lon = link_to_lat_lon(link)
        if lon is not None:
            located = True
            # print("\t", lat, lon)
            marker = Marker()
            marker.text = describe_issue(repo, title, number, label_names)
            marker.lat = lat
            marker.lon = lon

            if active:
                active_markers.insert(0, marker)
            if not_dead:
                not_dead_markers.insert(0, marker)
            if success:
                succesful_markers.insert(0, marker)

    if not located and (active or not_dead) and locatable:
        complain_about_issue_with_missing_location(description, label_names)

def github_link(repo, number):
    return "https://github.com/" + repo + "/issues/" + str(number)

def describe_issue(repo, title, number, label_names):
    text = title.replace("\"", "\\\"")
    link = github_link(repo, number)
    text += " <a href=" + link + ">#" + str(number) + "</a>"
    text += "<br />"
    for label in label_names:
        text += label + "<br />"
    return text

def write_markers_to_file(file, markers):
    for marker in markers:
        file.write(get_marker(marker.text, marker.lat, marker.lon))

def write_markers_to_standalone_file(filename, markers, title):
    processed = open(filename, 'w')
    before = get_before(title)
    after = get_after()

    processed.write(before)
    write_markers_to_file(processed, markers)

    processed.write(after)
    processed.close()

def write_markers_to_data_file(filename, markers, title):
    processed = open(filename, 'w')
    write_markers_to_file(processed, markers)
    processed.close()

main()
