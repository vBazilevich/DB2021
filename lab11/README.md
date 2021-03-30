# Lab 11 queries

## Task 1
**Filter:** `{}`

## Task 2
**Filter:** `{}`

**Project:** 
`{
    restaurant_id: 1,
    name: 1,
    borough: 1,
    cuisine: 1
}`

## Task 3
**Filter:** `borough: "Bronx"`

**Limit:** 5

## Task 4
**Filter:**
```
{ $or: [
    {
      cuisine: { $not: {$regex: /American\s*/}, $not: {$regex: /Chinese/}},
    }, 
    {name: {$regex: /^Wil/}}
  ]
}
```

**Project:** `{restaurant_id:1, name: 1, cuisine: 1, borough: 1}`

## Task 5
**Filter:** 
```
{
    name: {
        $regex: /mon/
    }
}
```

**Project:**
```
{"address.coords":1, name: 1, cuisine: 1, borough: 1}
```
