#
# gtkui.py
#
# Copyright (C) 2009 Jesse Johnson <holocronweaver>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource

class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        component.get("Preferences").add_page("Ratio", self.glade.get_widget("ratio_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)

        self.ratio_status_bar_item = component.get('StatusBar').add_item(
            #TODO: Better icon.
            stock = gtk.STOCK_ADD,
            callback = self.on_ratio_status_bar_clicked,
            tooltip = _('Ratio = Total Downloads / Total Uploads)'))

        self.glade.signal_autoconnect({
            'on_reset_ratio_button_clicked': self.on_reset_ratio_button_clicked
        })

    def disable(self):
        component.get("Preferences").remove_page("Ratio")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

        component.get('StatusBar').remove_item(self.ratio_status_bar_item)

    def update(self):
        client.ratio.get_ratio_and_totals().addCallback(self.update_ratio_label)

    def on_apply_prefs(self):
        log.debug("applying prefs for Ratio")
        config = {
            'persistent': self.glade.get_widget("persistent").get_active(),
        }
        client.ratio.set_config(config)

    def on_show_prefs(self):
        client.ratio.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "Callback for on_show_prefs."
        self.glade.get_widget('persistent') \
                  .set_active(config['persistent'])

    def on_reset_ratio_button_clicked(self, widget):
        log.debug('on_reset_ratio_button_clicked')
        client.ratio.reset_ratio()

    def on_ratio_status_bar_clicked(self, widget, event):
        pass

    def update_ratio_label(self, ratio_and_totals):
        self.ratio_status_bar_item.set_text('%0.1f (%0.1f/%0.1f GiB)' % ratio_and_totals)
