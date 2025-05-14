# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [0.13.2](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.13.1...v0.13.2) (2025-05-14)


### Bug Fixes

* **templates:** add lang tag and description meta tag ([bb4d7af](https://github.com/acdh-oeaw/apis-bibsonomy/commit/bb4d7af642a74f0ace57b2950bb143e13448d31d))
* **templates:** add missing closing div ([45f8f16](https://github.com/acdh-oeaw/apis-bibsonomy/commit/45f8f16cc49d8bf4e14d99541571958a29cd0e62))
* **templates:** drop use of entity reference ([2ac5749](https://github.com/acdh-oeaw/apis-bibsonomy/commit/2ac5749f327c02fff4b65d20151929f2ab1d9185))
* **templates:** format templates according to djlint ([70cd586](https://github.com/acdh-oeaw/apis-bibsonomy/commit/70cd586646e1b36a06e8e79c57bb8d921aec502a))

## [0.13.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.13.0...v0.13.1) (2024-12-16)


### Bug Fixes

* **models:** return empty dict if bibtex is missing ([6205894](https://github.com/acdh-oeaw/apis-bibsonomy/commit/62058946c0e1a3c0e9200e988eecaed14f84e2cc))

## [0.13.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.12.1...v0.13.0) (2024-12-12)


### Features

* move from bootstrap modal to standard dialog ([f177d21](https://github.com/acdh-oeaw/apis-bibsonomy/commit/f177d21961259443c8a892bd112389571d4b2788))

## [0.12.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.12.0...v0.12.1) (2024-11-27)


### Bug Fixes

* **models:** create wrapper around bibtex lookup ([66ac860](https://github.com/acdh-oeaw/apis-bibsonomy/commit/66ac860075549846862c5c39fc863501240bc944))

## [0.12.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.11.0...v0.12.0) (2024-10-11)


### Features

* **models:** change field type from TextField to JSONField ([c8b2609](https://github.com/acdh-oeaw/apis-bibsonomy/commit/c8b26097b58ddaa4d2c5d174014ae2ebf5606321))


### Bug Fixes

* **models:** replace custom method with GenericForeignKey ([a5c7997](https://github.com/acdh-oeaw/apis-bibsonomy/commit/a5c79978a54be1a2d7d2a27f55719aa94802b95c))

## [0.11.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.10.0...v0.11.0) (2024-08-26)


### ⚠ BREAKING CHANGES

* **forms:** drop unused form
* **templatetags:** drop unused templatetags

### Features

* **templates:** add edit button to reference list template ([9c9f232](https://github.com/acdh-oeaw/apis-bibsonomy/commit/9c9f2322c336e652c086ae4f814c0e2122f9b599))
* **templates:** add link to referenced object above reference form ([27aaf96](https://github.com/acdh-oeaw/apis-bibsonomy/commit/27aaf966021a8358f3d5730f6217d86e883d6f3d))
* **templates:** replace term delete with material symbol ([0d3d601](https://github.com/acdh-oeaw/apis-bibsonomy/commit/0d3d601ca77fdc0b042c69989c76330d14ebc92d))
* **views:** add ReferenceUpdateView for editing exising references ([df36657](https://github.com/acdh-oeaw/apis-bibsonomy/commit/df36657b05d32abd0c5da9910efbdad759ab57b7))


### Bug Fixes

* **forms:** drop use of apis listselect2 override ([20644b8](https://github.com/acdh-oeaw/apis-bibsonomy/commit/20644b80a12211771a63f31ae4b40716cb31c6a7))
* **forms:** set choices of Select2 widget ([5add6fa](https://github.com/acdh-oeaw/apis-bibsonomy/commit/5add6fa6ef2a48a055b72c28ed7d63fcbad1b348))
* **models:** always update bibsonomy field when saving Reference ([be6a403](https://github.com/acdh-oeaw/apis-bibsonomy/commit/be6a4030418d102fac36115e4c627343031c43b9))


### Code Refactoring

* **forms:** drop unused form ([a64fde3](https://github.com/acdh-oeaw/apis-bibsonomy/commit/a64fde364d6b73ef5926994dc691a8dcac0bccfa))
* **templatetags:** drop unused templatetags ([cec417b](https://github.com/acdh-oeaw/apis-bibsonomy/commit/cec417b58730716171a9b434edabeb7a21838d00))

## [0.10.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.9.1...v0.10.0) (2024-08-26)


### Features

* **commands:** add management command to update all bibtex fields ([36eddd6](https://github.com/acdh-oeaw/apis-bibsonomy/commit/36eddd6bf33c46c94810d9736f1213f667e55502))
* replace feather svg with material svg ([4904c64](https://github.com/acdh-oeaw/apis-bibsonomy/commit/4904c64aa06113886e8c190fd508acb8b0d6af0c))


### Bug Fixes

* **apis_view:** set the permission class of the ReferenceViewSet ([2ac0b68](https://github.com/acdh-oeaw/apis-bibsonomy/commit/2ac0b6841f74610188f58487024c62f96952f8ec))
* drop htmx loading in the templates - it should be done globally ([181852b](https://github.com/acdh-oeaw/apis-bibsonomy/commit/181852b17b0210951a2bd73b2f03a9bbb3aafb8c))
* **utils:** use cache in get_bibtex_from_url ([180fc93](https://github.com/acdh-oeaw/apis-bibsonomy/commit/180fc93256d69c7ca847f798d8deb59c82dc5673))
* **views:** set htmx to use API delete endpoint ([af585ff](https://github.com/acdh-oeaw/apis-bibsonomy/commit/af585ff49ffd14f65d3780a2589b90001cdf36c1))

## [0.9.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.9.0...v0.9.1) (2024-06-10)


### Bug Fixes

* **build:** set README.md as the readme in pyproject.toml ([763fe37](https://github.com/acdh-oeaw/apis-bibsonomy/commit/763fe37d1b31e7d53750ccd912ee86fa174f6204))

## [0.9.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.8.1...v0.9.0) (2024-06-10)


### Features

* add a basic api endpoint for references ([8158819](https://github.com/acdh-oeaw/apis-bibsonomy/commit/81588198e4483e50aadac4d3e6f04622bfcbd654)), closes [#49](https://github.com/acdh-oeaw/apis-bibsonomy/issues/49)
* add admin integration for references ([428999e](https://github.com/acdh-oeaw/apis-bibsonomy/commit/428999e4130ef6a471f7710df4b5af81f1b84a35))

## [0.8.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.8.0...v0.8.1) (2024-01-24)


### Bug Fixes

* allow delete with htmx ([5e58fc4](https://github.com/acdh-oeaw/apis-bibsonomy/commit/5e58fc40dcd9318116f1c68b2b8206dd00d0370f))

## [0.8.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.7.2...v0.8.0) (2023-11-14)


### Features

* add link_to_reference_on templatetag ([9e960fc](https://github.com/acdh-oeaw/apis-bibsonomy/commit/9e960fcd99766c9c30360ab646c53bf8066e50ad))
* implement referenceonlist view ([8f47ddb](https://github.com/acdh-oeaw/apis-bibsonomy/commit/8f47ddb99c8e8276138b3d747bec9d7cebd6c545))
* **ReferenceOnListView:** add form to add new reference ([3fff43c](https://github.com/acdh-oeaw/apis-bibsonomy/commit/3fff43cfb56e3fa13ba94b35d4149b72fabcda13))
* **ReferenceOnListView:** load last added bibsononmy title in form ([04519be](https://github.com/acdh-oeaw/apis-bibsonomy/commit/04519be58aa448cba7e267417957de64391c4ff6))
* **ReferenceOnListView:** split view into multiple views ([f14ae9e](https://github.com/acdh-oeaw/apis-bibsonomy/commit/f14ae9e318c919a21e689a621c2fbb0870fde2fc))


### Bug Fixes

* add basic auth check ([c1279fa](https://github.com/acdh-oeaw/apis-bibsonomy/commit/c1279fa1b229f211301845fba1a7f7df13148f5c))

## [0.7.2](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.7.1...v0.7.2) (2023-11-06)


### Bug Fixes

* **deps:** add jmespath to dependencies ([7a725ad](https://github.com/acdh-oeaw/apis-bibsonomy/commit/7a725ad7af3b76ec308875544b3069ba17c4421d)), closes [#38](https://github.com/acdh-oeaw/apis-bibsonomy/issues/38)

## [0.7.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.7.0...v0.7.1) (2023-06-09)


### Bug Fixes

* typo in template ([85dac48](https://github.com/acdh-oeaw/apis-bibsonomy/commit/85dac483db61c31847146fe03b3de2d5a1677745))

## [0.7.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.6.0...v0.7.0) (2023-05-22)


### Features

* move bibtex fetching to utils ([b0af808](https://github.com/acdh-oeaw/apis-bibsonomy/commit/b0af8083d015f78101c96cb11b898c8f822a5c2a))

## [0.6.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.5.0...v0.6.0) (2023-05-17)


### Features

* add a detail link to the reference listings ([099acbd](https://github.com/acdh-oeaw/apis-bibsonomy/commit/099acbde9c671d9876e553658a1db2cc5cc6cd02))

## [0.5.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.4.1...v0.5.0) (2023-04-27)


### Features

* add convenience views to bibsonomy ([d30e68f](https://github.com/acdh-oeaw/apis-bibsonomy/commit/d30e68f9f4137754676e94a015f0442138d63cf6))


### Bug Fixes

* Set the default_auto_field ([55465d2](https://github.com/acdh-oeaw/apis-bibsonomy/commit/55465d271f1b47031c824dadf3613bd31857d35a))

## [0.4.1](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.4.0...v0.4.1) (2023-04-04)


### Bug Fixes

* fixes issue [#24](https://github.com/acdh-oeaw/apis-bibsonomy/issues/24) ([0586439](https://github.com/acdh-oeaw/apis-bibsonomy/commit/058643906e9feb9a4208e8d93eb50057e7dbb413))

## [0.4.0](https://github.com/acdh-oeaw/apis-bibsonomy/compare/v0.3.6...v0.4.0) (2023-04-04)


### Features

* fixes dependencies and removes apis-core ([d6727a6](https://github.com/acdh-oeaw/apis-bibsonomy/commit/d6727a6b9bc68bd1bf2d431e4edf8b6e96480f3e))
