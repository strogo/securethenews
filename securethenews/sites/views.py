from django.core.mail import mail_admins, send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

import json

from .forms import PledgeForm
from .models import Site
from .wagtail_hooks import PledgeAdmin


def index(request):
    sites = Site.objects.all()
    return render(request, 'sites/index.html', dict(
        sites_json=json.dumps([site.to_dict() for site in sites]),
    ))


def site(request, slug):
    site = get_object_or_404(Site, slug=slug)
    latest_scan = site.scans.latest()
    return render(request, 'sites/site.html', dict(
        site=site,
        scan=latest_scan,
    ))


def pledge(request):
    if request.method == 'POST':
        form = PledgeForm(request.POST)
        if form.is_valid():
            new_pledge = form.save()

            # Notify the admins that a new pledge is ready for review
            admin_notification_subject = 'New Pledge: {}'.format(
                new_pledge.site.name
            )
            # Get the wagtailmodeladmin PledgeAdmin so we can derive the edit
            # url for the newly submitted pledge.
            pledge_admin = PledgeAdmin()
            ctx = {
                'site': new_pledge.site,
                'moderation_link': request.build_absolute_uri(
                    pledge_admin.url_helper.get_action_url(
                        'edit',
                        new_pledge.pk
                    )
                ),
            }
            admin_notification_body = render_to_string(
                'sites/pledge_submitted_admin_notification_email.txt',
                ctx
            )
            mail_admins(
                admin_notification_subject,
                admin_notification_body
            )

            # Send a confirmation email to the user who submitted the pledge
            confirmation_subject = \
                "Thanks for pledging to secure your site on Secure the News!"
            confirmation_body = render_to_string(
                'sites/pledge_submitted_confirmation_email.txt'
            )
            send_mail(
                subject=confirmation_subject,
                message=confirmation_body,
                from_email='contact@securethe.news',
                recipient_list=[new_pledge.contact_email,]
            )

            return HttpResponseRedirect(reverse('sites:pledge_thanks'))
    else:
        form = PledgeForm()

    return render(request, 'sites/pledge.html', {'form': form})


def pledge_thanks(request):
    return render(request, 'sites/pledge_thanks.html')
