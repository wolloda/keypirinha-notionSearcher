# Keypirinha Plugin: notionSearcher

This is notionSearcher, a plugin for the [Keypirinha](http://keypirinha.com) launcher.

It is used to quickly open Notion pages.

## Download

[https://github.com/wolloda/keypirinha-notionSearcher/releases](https://github.com/wolloda/keypirinha-notionSearcher/releases)

## Install

### Plugin

Once the `Notion.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


### Notion access rights

To access your Notion pages, following steps are required:

* Visit ["My integrations"](https://www.notion.so/my-integrations)
* Create a new integration
	* from *Content Capability*, onlye *Read content* is necessary
	* no *Comment Capabilities* needed
	* no *User Capability* needed
* Allow the newly created integration to access your pages:
	* Press the `...` in the upper right corner of a page
	* In `Connections` click on *Add connections* and select the newly created integration
	* Do this for pages you want to have available in the plugin
		* Connections are inherited by child pages - therefore it must be done only with parent
			pages
		* If you want to have all pages available in the Package, do this for all root Pages in the
			workspace
* Copy *Internal Integration Token* and paste it in the `[var]` section of `Notion.ini` user config file (`Keypirinha: Configure Package: Notion` comes handy)

## Options

* [main]
	* `show_parent_page_name` — show name of the page's parent page in the result
	* `skip_untitled_pages` — skip pages that don't have a name (i.e. unnamed database entries)
	* `download_icons` — download and show page icons
	* `global_results` — pages shown in global catalogue without needing to query `Notion: Find page` to search page names.
* [var]
	* `notion_secret` —  integration secret that allows this plugin to work

## Usage

Following commands are created:
* `Notion: Find page` searches for pages by their name
	* when `Tab` is pressed on a result, it allows to *open a page in a browser*, *open a page in
		the Notion app*, and *copy URL to page*
* `Notion: Reload pages` catalog of pages does not refresh automatically as it can take quite some time, making this package unusable in the process. Therefore runing this command is needed to index new pages and reindex changes (renamed pages, icon changes, etc.) in the workspace. Works like `Keypirinha: Refresh Catalog: Notion` command.
* `Notion: Remove images` removes downloaded page icons

## License

This package is distributed under the terms of the MIT license.