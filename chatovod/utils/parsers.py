# -*- encoding: UTF-8 -*-

import re

from bs4 import BeautifulSoup, SoupStrainer

# Makes BeautifulSoup parse only ban entry elements
only_ban_entries = SoupStrainer("label")

# RegEx to extract informations from the ban list.
# This is meant to be used for tt(Tatar) language.
# az(Azeri) is the least likely to break, however
# the nickname of the banned user doesn't show up in it(server-side bug).
# Tatar seems to be the second most reliable option
# since it is not used that much in Chatovod,
# considering the default language URL redirection.
# ### Example ###
# 'Fluffy дат(тан) 12.31.2016 12.50 AM чаклы (120 minutes) '
# 'модераторларга EvilModerator, комментарий: I banned you'

parse_ban_message = re.compile(
    r"""(?P<nickname>.{1,25}?) # A nickname must have up to 25 characters
        ([ ]\S*[ ])            # Single space, non-space characters, single space
        (?P<month>[0-9]{1,2})  # Month
        .(?P<day>[0-9]{1,2})   # Day
        .(?P<year>[0-9]{1,4})  # Year
        [ ]                    # Space
        (?P<hour>[0-9]{1,2}).(?P<minute>[0-9]{1,2}) # Hour and minute
                                                    # in 12-hour clock format
        [ ]
        (?P<period>AM|PM) # Period of the day - AM or PM
        ([ ]\S*[ ])
        \(                        # The following will be wrapped in parenthesis
            (?P<duration>[0-9,]+) # Duration of the ban in minutes
            ([ ]\w+)              # Space, word minutes
        \)                        # Close parenthesis
        ([ ]\S*[ ])
        (?P<author>.{1,25}?)  # Nickname of the author of the ban
        (,[ ]комментарий:[ ]) # We need this to know when the author nickname
                              # ends and when the ban comment starts
        (?P<comment>(.|\n){,256}?)$""",
    re.VERBOSE,
)


def patch_ban_info(ban_info, ban_data):
    # Add 'id' field contained in the child element
    # And strips the commas out of the duration string
    ban_info["id"] = ban_data["value"]
    ban_info["duration"] = join_all_numbers(ban_info["duration"])

    return ban_info


def generate_bans_info_from_html(html_ban_list, parser="html.parser"):
    """An utility function for parsing HTML ban lists.

    :param ban_list: the HTML ban list returned by the Chatovod API.
    """

    # A soup containing all ban entry elements found in the HTML string
    ban_entries_soup = BeautifulSoup(html_ban_list, parser, parse_only=only_ban_entries)

    for ban_entry in ban_entries_soup:
        # Match the child element which contains the ID of the ban
        # Used to identify valid ban entries
        ban_data = ban_entry.find(class_="banEntry")
        if ban_data is None:
            continue

        ban_info_match = parse_ban_message.search(ban_entry.text)
        ban_info = ban_info_match.groupdict()
        patched_ban_info = patch_ban_info(ban_info, ban_data)

        yield patched_ban_info


def join_all_numbers(string, separator=""):
    return separator.join([char for char in string if char.isdigit()])
