# Keypirinha Plugin: Notion

This is a Notion, a plugin for the [Keypirinha](http://keypirinha.com) launcher.

It allows to search and open Notion pages.

## Download

[https://github.com/wolloda/keypirinha-notionSearcher/releases](https://github.com/wolloda/keypirinha-notionSearcher/releases)

## Install

Once the `Notion.keypirinha-package` file is installed,
move it to the `InstalledPackage` folder located at:

* `Keypirinha\portable\Profile\InstalledPackages` in **Portable mode**
* **Or** `%APPDATA%\Keypirinha\InstalledPackages` in **Installed mode** (the
  final path would look like
  `C:\Users\%USERNAME%\AppData\Roaming\Keypirinha\InstalledPackages`)


To access your Notion pages, following steps are required:

* Visit ["My integrations"](https://www.notion.so/my-integrations)
* Create a new integration
	* only necessary *Content Capability* is *Read content*
	* no *Comment  Capabilities* needed
	* no *User Capability* needed
* Allow the newly created integration to access your pages:
	* Press the `...` in the upper right corner of a page
	* In `Connections` click on *Add connections* and select the integration
	* Do this for pages that are going to be searched
		* Only the topmost pages has to be connected - all pages in them inherit this behaviour
* Copy *Internal Integration Token* and paste it in the `[var]` section of `Notion.ini` config file

## Options

* [main]
	* `show_parent_page_name` — show page's parent page in the result
	* `skip_untitle_pages` — show pages that don't have a name (good for unnamed database entries)
	* `download_icons` — download and show page icons
* [var]
	* `notion_secret` —  integration secret that allows this plugin to work

## Usage

Following commands are created:
* `Notion: Find page` searches for pages by their name
	* when `Tab` is pressed on a result, it allows to *open a page in a browser*, *open a page in
		an installed Notion app*, and *copy URL to page*
* `Notion: Reload pages` catalog of pages does not refresh automatically, therefore runing this
	command is needed to index new pages and reindex changes (renaming pages, etc.)
* `Notion: Remove images` removes downloaded page icons

## License

This package is distributed under the terms of the MIT license.
