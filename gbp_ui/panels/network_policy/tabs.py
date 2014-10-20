#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Ronak Shah

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from horizon import tabs

from openstack_dashboard.dashboards.project.instances.tables import is_deleting
from openstack_dashboard import api

from gbp_ui import client
import tables


class L3PolicyDetailsTab(tabs.Tab):
	name = _("L3 Policy Details")
	slug = "l3_policy_details"
	template_name = "project/endpoint_groups/_l3_policy_details.html"
	failure_url = reverse_lazy('horizon:project:endpoint_group:index')

	def get_context_data(self,request):
		l3policy_id = self.tab_group.kwargs['l3policy_id']
		try:
			l3policy = client.l3policy_get(request,l3policy_id)
		except Exception:
			exceptions.handle(request, _('Unable to retrieve l3 policy details.'), redirect=self.failure_url)
		return {'l3policy':l3policy}
 
 
class L3PolicyDetailsTabs(tabs.TabGroup):
	slug = "l3policy_tabs"
	tabs = (L3PolicyDetailsTab,) 
 
class L3PolicyTab(tabs.TableTab):
	table_classes = (tables.L3PolicyTable,)
	name = _("L3 Policy")
	slug = "l3policy"
	template_name = "horizon/common/_detail_table.html"

	def get_l3policy_table_data(self):
		policies = []
 		try:
			tenant_id = self.request.user.tenant_id
			policies = client.l3policy_list(self.request,tenant_id=tenant_id)
		except Exception:
			policies = []
			exceptions.handle(self.tab_group.request,
							_('Unable to retrieve l3 policy list.'))
		return policies 

class L3PolicyTabs(tabs.TabGroup):
    slug = "l3policy_tab"
    tabs = (L3PolicyTab,)
    sticky = True
 
