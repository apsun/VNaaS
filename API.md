# VNaaS REST API

All API paths are prefixed with `/api/v1`. For example, the URL
for querying novels is `/api/v1/novels`.

Query parameters should be added using the standard format,
`base_url?key1=value1&key2=value2`.

All novel and character ID numbers correspond to their
entries on [VNDB](https://vndb.org/).

Note that Ruby text (e.g. Furigana) is included in the output and is
expressed in format `[ruby|base]`. For example: `[かんじ|漢字]`.


## `/novels`

Returns a list of available visual novels. Returns
an empty list if no novels match the query parameters.

Query parameters:

- `character_id`: Optional. Filters results by novels containing the specified character.
- `name`: Optional. Filters results by novels with the specified name.

Example output:

```JSON
[
    {
        "id": 1234,
        "name": "Hoshizora no Memoria",
        "characters": [
            {
                "id": 9999,
                "name": "Mare S Ephemeral"
            },
            {
                "id": 10000,
                "name": "Asuho Minahoshi"
            }
        ]
    },
    {
        "id": 1235,
        "name": "Irotoridori no Sekai",
        "characters": [
            {
                "id": 5000,
                "name": "Shinku Nikaidou"
            },
            {
                "id": 5001,
                "name": "Mio Kisaragi"
            }
        ]
    }
]
```


## `/novels/<novel id>`

Returns information about a single visual novel. Returns 404 if
the specified novel does not exist.

Example output:

```JSON
{
    "id": 1234,
    "name": "Hoshizora no Memoria",
    "characters": [
        {
            "id": 9999,
            "name": "Mare S Ephemeral"
        },
        {
            "id": 10000,
            "name": "Asuho Minahoshi"
        }
    ]
}
```


## `/characters`

Returns a list of characters in the database. Returns
an empty list if no characters match the query parameters.

Query parameters:

- `novel_id`: Optional. Filters results by characters from the specified novel.
- `name`: Optional. Filters results by characters with the specified name.

If you do not provide the query parameter, all characters
in the database will be returned.

Example output:

```JSON
[
    {
        "id": 9999,
        "name": "Mare S Ephemeral",
        "novels": [
            {
                "id": 1234,
                "name": "Hoshizora no Memoria"
            },
            {
                "id": 1236,
                "name": "Hoshizora no Memoria Eternal Heart"
            }
        ]
    },
    {
        "id": 5000,
        "name": "Shinku Nikaidou",
        "novels": [
            {
                "id": 1235,
                "name": "Irotoridori no Sekai",
            },
            {
                "id": 1237,
                "name": "Irotoridori no Hikari"
            }
        ]
    }
]
```


## `/characters/<character id>`

Returns information about a single character. Returns 404 if
the specified character does not exist.

Example output:

```JSON
{
    "id": 9999,
    "name": "Mare S Ephemeral",
    "novels": [
        {
            "id": 1234,
            "name": "Hoshizora no Memoria"
        },
        {
            "id": 1236,
            "name": "Hoshizora no Memoria Eternal Heart"
        }
    ]
}
```


## `/random_quote`

Returns a random quote from the database. Returns 404 if there
are no quotes matching the query parameters.

Query parameters:

- `novel_ids`: Optional. Filters results by quotes from the specified novels (comma-separated list).
- `character_ids`: Optional. Filters results by quotes from the specified characters (comma-separated list).
- `contains`: Optional. Filters results by quotes containing the specified text.

Example output:

```JSON
{
    "text": "Bakabaka",
    "character": {
        "id": 9999,
        "name": "Mare S Ephemeral"
    },
    "novel": {
        "id": 1234,
        "name": "Hoshizora no Memoria"
    }
}
```
