# -*- coding: utf-8 -*-
from .requester import OCSRequester, WebDAVRequester, DeckRequester
from .api_wrappers import OCS_API_CLASSES, WEBDAV_CLASS, DECK_CLASS

class NextCloud(object):

    def __init__(self, endpoint, user, password, json_output=True):
        self.user = user
        self.query_components = []

        ocs_requester = OCSRequester(endpoint, user, password, json_output)
        webdav_requester = WebDAVRequester(endpoint, user, password)
        deck_requester = DeckRequester(endpoint, user, password, json_output)

        self.functionality_classes = [api_class(ocs_requester) for api_class in OCS_API_CLASSES]
        self.functionality_classes.append(WEBDAV_CLASS(webdav_requester, json_output=json_output))
        self.functionality_classes.append(DECK_CLASS(deck_requester))

        for functionality_class in self.functionality_classes:
            for potential_method in dir(functionality_class):
                if(
                    potential_method.startswith('_')
                    or not callable(getattr(functionality_class, potential_method))
                ):
                    continue
                setattr(self, potential_method, getattr(functionality_class, potential_method))

    def get_connection_issues(self):
        """
        Return Falsy falue if everything is OK, or string representing
        the connection problem (bad hostname, password, whatever)
        """
        try:
            response = self.get_user(self.user)
        except Exception as e:
            return str(e)

        if not response.is_ok:
            return response.meta["message"]
