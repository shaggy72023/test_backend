import bb_comment.services.comment
import json

from django.views.generic import View

from utils.api.mixins import APIMixin


class Comment(APIMixin, View):

    def post(self, request, parameters):
        parameters = json.loads(parameters)
        return bb_comment.services.comment.create(request, parameters)
