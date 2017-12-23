#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from bitbay import BitBay
import time

class ComboBoxWindow(Gtk.Window):

    def __init__(self):
        self.bb=BitBay()
        self.fields=["time","bid", "last", "ask", "volume", "average", "max", "min", "vwap"]
        self.pair=''
        Gtk.Window.__init__(self, title="BitBay Tickers")

        self.set_default_size(200, 200)
        self.set_border_width(10)
        self.set_icon_from_file('bitcoin.png')
	
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        country_store = Gtk.ListStore(str)
        countries = self.bb.getPairs()
        for country in countries:
            country_store.append([country])

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(country_combo, True, False, False)

        self.liststore = Gtk.ListStore(str, str)
        for field in self.fields:
                self.liststore.append([field, ""])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Type", renderer_text, text=0)
        treeview.append_column(column_text)


        column_text = Gtk.TreeViewColumn("Value", renderer_text, text=1)
        treeview.append_column(column_text)

        vbox.pack_end(treeview, True, True, True)

        self.button1 = Gtk.Button(label="Refresh")
        self.button1.connect("clicked", self.on_button1_clicked)
        vbox.pack_end(self.button1, True, True, 6)

        self.add(vbox)

    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            self.pair = model[tree_iter][0]
            currencies = self.pair.split('/')
            ticker = self.bb.getTicker(currencies[0], currencies[1])
            self.liststore[0][1] = time.ctime(self.bb.lastTicker(currencies[0], currencies[1]))
            i=1
            for field in self.fields[1:]:
                self.liststore[i][1] = str(ticker[field])
                i+=1

    def on_button1_clicked(self, widget):
        currencies = self.pair.split('/')
        ticker = self.bb.getTicker(currencies[0], currencies[1])
        self.liststore[0][1] = time.ctime(self.bb.lastTicker(currencies[0], currencies[1]))
        i=1
        for field in self.fields[1:]:
            self.liststore[i][1] = str(ticker[field])
            i+=1

win = ComboBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
