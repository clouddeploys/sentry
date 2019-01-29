from __future__ import absolute_import

from rest_framework.response import Response

from sentry.api.base import DocSection
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.helpers.environments import environment_visibility_filter_options
from sentry.api.serializers import serialize
from sentry.models import EnvironmentProject
from sentry.utils.apidocs import scenario, attach_scenarios


@scenario('RetrieveEnvironmentsForProject')
def retrieve_environments_for_project_scenario(runner):
    runner.request(
        method='GET',
        path='/projects/%s/%s/environments/' %
        (runner.org.slug, runner.default_project.slug)
    )


class ProjectEnvironmentsEndpoint(ProjectEndpoint):
    doc_section = DocSection.PROJECTS

    @attach_scenarios([retrieve_environments_for_project_scenario])
    def get(self, request, project):
        queryset = EnvironmentProject.objects.filter(
            project=project,
        ).exclude(
            # HACK(mattrobenolt): We don't want to surface the
            # "No Environment" environment to the UI since it
            # doesn't really exist. This might very likely change
            # with new tagstore backend in the future, but until
            # then, we're hiding it since it causes more problems
            # than it's worth.
            environment__name='',
        ).select_related('environment').order_by('environment__name')

        visibility = request.GET.get('visibility', 'visible')
        if visibility not in environment_visibility_filter_options:
            return Response({
                'detail': u'Invalid value for \'visibility\', valid values are: {!r}'.format(
                    environment_visibility_filter_options.keys(),
                ),
            }, status=400)

        add_visibility_filters = environment_visibility_filter_options[visibility]
        queryset = add_visibility_filters(queryset)

        return Response(serialize(list(queryset), request.user))
