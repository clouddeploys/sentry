from __future__ import absolute_import

from django.views.generic import View

from sentry.models import Group, Organization, Project, ProjectTeam, Team

from .mail import MailPreview


class DebugNewUserFeedbackEmailView(View):
    def get(self, request):
        org = Organization(
            id=1,
            slug='organization',
            name='My Company',
        )
        team = Team(
            id=1,
            slug='team',
            name='My Team',
            organization=org,
        )
        project = Project(
            id=1,
            organization=org,
            slug='project',
            name='My Project',
        )
        ProjectTeam(
            project=project,
            team=team
        )
        group = Group(
            id=1,
            project=project,
        )

        return MailPreview(
            html_template='sentry/emails/activity/new-user-feedback.html',
            text_template='sentry/emails/activity/new-user-feedback.txt',
            context={
                'group': group,
                'report': {
                    'name': 'Homer Simpson',
                    'email': 'homer.simpson@example.com',
                    'comments': 'I hit a bug.\n\nI went to https://example.com, hit the any key, and then it stopped working. DOH!',
                },
            },
        ).render(request)
