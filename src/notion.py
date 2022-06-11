# Keypirinha launcher (keypirinha.com)

import os
import time

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

import urllib.request

# from .lib import requests
# from .lib import urllib3

from .notion_searcher import NotionSearcher

class Notion(kp.Plugin):
    """
    Search and launch Notion pages from Keypirinha

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """

    NOTION_PAGE_CATEGORY = kp.ItemCategory.USER_BASE + 1
    APP_URI_HANDLER = "notion://"

    DEFAULT_ICON = "res://Notion/img/notion_logo.png"

    ACTION_OPEN_BROWSER = "open_browser"
    ACTION_OPEN_APP = "open_app"
    ACTION_COPY_URL = "copy_url"

    def __init__(self):
        super().__init__()
        self._debug = True
        self._pages = []

    def on_start(self):
        self._read_config()
        self._create_actions()
        self._notion_searcher = NotionSearcher(self._NOTION_SECRET)

        # self._clear_images()

        self._refresh_pages()

        self.set_default_icon(self.load_icon(self.DEFAULT_ICON))

    def on_catalog(self):
        catalog = [
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Notion: Find page",
                short_desc="Find pages by their names",
                target="find_pages",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.KEEPALL
            ),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Notion: Reload pages",
                short_desc="Reload list of pages",
                target="reload_pages",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS)
        ]

        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if items_chain and items_chain[-1].target() == 'find_pages':
            self.set_suggestions(
                self._generate_suggestions()
            )

    def on_execute(self, item, action):
        if item.category() not in (self.NOTION_PAGE_CATEGORY, kp.ItemCategory.KEYWORD):
            return

        if item.category() == kp.ItemCategory.KEYWORD:
            if item.target() == "reload_pages":
                self._refresh_pages()
                return

        # open page in browser
        if not action or action.name() == self.ACTION_OPEN_BROWSER:
            kpu.web_browser_command(private_mode=False, url=item.target(), execute=True)
            return

        # open page in desktop app
        if action.name() == self.ACTION_OPEN_APP:
            kpu.shell_execute(f"{self.APP_URI_HANDLER}{item.target()[8:]}")
            return

        # copy page URL
        if action.name() == self.ACTION_COPY_URL:
            kpu.set_clipboard(item.target())
            return

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        self._read_config()
        self.on_catalog()

        # self._clear_images()
        self._refresh_pages()

    def _read_config(self):
        settings = self.load_settings()
        self._NOTION_SECRET = settings.get("notion_secret", "var", unquote=True)
        self._MATCH_PARENTS = settings.get_bool("show_parent_page_name", "var")
        self.clear_actions()

    def _create_actions(self):
        actions = [
            self.create_action(name=self.ACTION_OPEN_BROWSER,
                               label="Open page",
                               short_desc="Open page in browser"),
            self.create_action(name=self.ACTION_OPEN_APP,
                               label="Open page in client",
                               short_desc="Notion application must be installed"),
            self.create_action(name=self.ACTION_COPY_URL,
                               label="Copy URL",
                               short_desc="Copy page URL to clipboard")
        ]
        self.set_actions(self.NOTION_PAGE_CATEGORY, actions)

    def _refresh_pages(self):
        start = time.time()
        self._pages = self._notion_searcher.search(self._MATCH_PARENTS)
        end = time.time()
        self.info(f"list of notion pages refreshed in {end - start} seconds")
        # self._download_icons()

    def _download_icons(self):
        for page in self._pages:
            if page["iconURL"]:
                try:
                    urllib.request.urlretrieve(page["iconURL"], f"{self.ICONS_CACHE_DIR}/{page['iconName']}")
                except:
                    self.err(f"{page['iconURL']} unavailable")

    def _generate_suggestions(self):
        suggestions = []

        if not self._pages:
            return []

        for suggestion in self._pages:
            icon_handle = None

            label = suggestion["name"]
            if suggestion["parent"]:
                label += f" ({suggestion['parent']})"

            suggestions.append(self.create_item(
                category=self.NOTION_PAGE_CATEGORY,
                label=label,
                short_desc=suggestion["url"],
                target=suggestion["url"],
                icon_handle=icon_handle,
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE
            ))

        return suggestions
