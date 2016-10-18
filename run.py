import requests
import requests_cache
import zikit_labels
import config
from leaflet import get_before, get_after, get_marker

requests_cache.install_cache(config.get_cache_name())
import json
import os
from os.path import join
import re

with open(join(os.environ['HOME'], '.github-oauth-read-token.json')) as f:  # TODO - create this file
    token = json.load(f)['token']

standard_headers = {'User-Agent': 'github-zikitator/0.0',
                    'Authorization': 'bearer {0}'.format(token)}


class Marker:
    pass


active_markers = []
not_dead_markers = []
succesful_markers = []

def main():
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
        issues_url = 'https://api.github.com/repos/{0}/issues'.format(repo)
        r = requests.get(issues_url,
                         params={'per_page': '100',
                                 'page': str(page),
                                 'state': state},
                         headers=standard_headers)
        if r.status_code != 200:
            raise Exception("HTTP status {0} on fetching {1}".format(
                r.status_code,
                issues_url))

        issues_json = r.json()
        if len(issues_json) == 0:
            break

        for issue in issues_json:
            process_issue(issue, inactive, closed, active, without_location, success)
        page += 1
    name = main_name
    write_markers_to_data_file(name+'.data', active_markers, name)
    write_markers_to_standalone_file(name+'.html', active_markers, name)
    name = main_name + '-all'
    write_markers_to_standalone_file(name+'.html', not_dead_markers, name)
    name = main_name + '-succesful'
    write_markers_to_standalone_file(name+'.html', succesful_markers, name)

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

def process_issue(issue, inactivating_labels, closing_labels, activating_labels, without_location, success_labels):
    number = issue['number']
    title = issue['title']
    labels = issue['labels']
    body = issue['body']

    description = str(number) + " " + title

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
            marker.text = describe_issue(title, number, label_names)
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


def describe_issue(title, number, label_names):
    text = title.replace("\"", "\\\"")
    link = "https://github.com/matkoniecz/Krakow/issues/" + str(number)
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
