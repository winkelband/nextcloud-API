# -*- coding: utf-8 -*-
from nextcloud.base import WithRequester


class Deck(WithRequester):
    API_URL = "/index.php/apps/deck/api/v1.0/boards"
    #SUCCESS_CODE = 

    def get_boards_text(self, options=False):
        """
        Retrieve a string of boards from the Nextcloud server
        :return: str
        """
        params = {
            'options': options,
        }
        return self.requester.get(params=params)

    def get_boards(self):
        """
        Retrieve a list of boards from boards text
        :return: dictionaries in list
        """
        board_list = self.get_boards_text()
        boards = []
        for b in board_text.full_data:
            board = {
                'id': b['id'],
                'title': b['title'],
                'owner': b['owner'],
                'color': b['color'],
                'archived': b['archived'],
                'labels': b['labels'],
                'acl': b['acl'],
                'permissions': b['permissions'],
                'users': b['users'],
                'shared': b['shared'],
                'deletedAt': b['deletedAt'],
            }
            boards.append(board)
        return(boards)

    def get_board_details(self, bid):
        """
        Retrieve details of one board
        :return:
        """
        return self.requester.get("{bid}".format(bid=bid))

    def get_stacks_text(self, bid):
        """
        Retrieve a string of stacks from the Nextcloud server
        :return: str
        """
        return self.requester.get("{bid}/stacks".format(bid=bid))

    def get_stacks(self, bid):
        """
        Retrieve a list of stacks from stacks text.
        Attribute "cards" is not getting returned.
        :return:
        """
        stacks_text = self.get_stacks_text(bid=bid)
        stacks = []
        for s in stacks_text.full_data:
            stack = {
                'id': s['id'],
                'title': s['title'],
                'boardId': s['boardId'],
                'deletedAt': s['deletedAt'],
                'lastModified': s['lastModified'],
                'order': s['order'],
            }
            stacks.append(stack)
        return stacks

    def get_labels_id(self, bid):
        """
        Retrieve a list of label ids.
        """
        board = self.get_board_details(bid)
        labels = board.full_data['labels']
        labels_id = [label['id'] for label in labels]
        return(labels_id)

    def get_label_details(self, bid, lid):
        """
        Retrieve attributes of one label:
            title, color, boardID, cardID: None, id
        """
        return self.requester.get("{bid}/labels/{lid}".format(bid=bid, lid=lid))

    def get_labels(self, bid):
        """
        Retrieve all labels with their attributes:
            title, color, boardID, cardID: None, id
        """
        label_list = self.get_board_details(bid)
        labels = []
        for label in label_list.full_data['labels']:
            label = {
                'id': label['id'],
                'title': label['title'],
                'color': label['color'],
                'boardId': label['boardId'],
                'cardId': label['cardId']
            }
            labels.append(label)
        return(labels)
     
    def create_label(self, bid,
                     title=None, color="31CC7C"):
        """
        Create label only if its title
        does not exist in other label.
        On Deck title does not have to be unique.
        Always return the label's id.
        """
        labels = self.get_labels(bid=bid)
        labels_title = [label['title'] for label in labels]
        if title in labels_title:
            label_id = [label['id'] for label in labels if label['title'] == title][0]
        else:
            self.requester.post("{bid}/labels".format(bid=bid), data=data)
            # API does not return the id
            # of the newly created label,
            # instead make a request.
            labels = self.get_labels(bid=bid)
            label_id = [label['id'] for label in labels if label['title'] == title][0]
        return label_id

    def add_card(self, bid, sid,
                 title=None, card_type='plain', order=None,
                 description=None, duedate=None):
        """
        If no order specified, the API will assign
        the next highest number, so the card will be
        the lowest one in the stack.
        """
        data = {
            'title': title,
            'type': card_type,
            'order': order,
            'description': description,
            'duedate': duedate,
        }
        return self.requester.post("{bid}/stacks/{sid}/cards".format(bid=bid, sid=sid),
                                                              data=data)

    def assign_label(self, bid, sid, cid, 
                     lid=None):
        """
        Assign a label (lid) to a card (cid)
        on a board (bid).
        param: bid of board, sid of stack, cid of card
        """
        data = {
            'labelId': lid,
        }
        return self.requester.put("{bid}/stacks/{sid}/cards/{cid}/assignLabel".format(bid=bid, sid=sid, cid=cid),
                                                                               data=data)
