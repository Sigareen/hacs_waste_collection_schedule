# Ikast-Brande Kommune

Support for schedules provided by [Ikast-Brande Kommune](https://skrald.ikast-brande.dk/), Denmark.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
    sources:
    - name: ikastbrande_dk
      args:
        id: See description
```

### Configuration Variables

**id**  
_(String) (required)_

## Example

```yaml
waste_collection_schedule:
    sources:
    - name: ikastbrande_dk
      args:
        address_id: "12345"
```

## How to get the id

Go to the [Tømningsinformation](https://skrald.ikast-brande.dk/Tomningsinfo) page, enter your address.

In the URL (web page address) copy the number after `AdresseId=`

`I.e.` [`https://skrald.ikast-brande.dk/Tomningsinfo?AdresseId=12345&siteType=R&kom=0&lang=dk`](https://skrald.ikast-brande.dk/Tomningsinfo?AdresseId=12345&siteType=R&kom=0&lang=dk)

Then it's the `12345` part used in the integration
