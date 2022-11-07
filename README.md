# python-json-semantic-versioning-poc


Simple Proof of Concept for migrating nested JSON versions.

All minor version changes are non-breaking (i.e. don't affect the schema's backward compatibility).

All major version changes are breaking (i.e. affect the schema's backward compatibility).

Major version changes include:
- Deletion of fields
- Renaming of fields

Any non-optional additive changes cannot be added to this list since the migration cannot be automated and require user input.

## TODO

- [ ] Improve current schema versioning handling
- [ ] Add further tests for edge cases