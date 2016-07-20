# resource_allocator

Resource allocator module is providing the server (cpus ) as per the user needs. Wriiten in python 2.7 + 
  - N cpu for H hours Price(?)
  - N cpu for H houurs with maximum willing Price to pay
  - N cpu for H hours with max willing Price 

### Todos
 - Write UnitTests
 - Refactor the code to work in optimal way

License
----

MIT

### How to use:

instances = It's an dict of dict of containing data center server information.
```sh
$ import resalloc
$ resalloc.ResourceAllocator().get_costs(instances, hours, cpu, price)

Example:
$ resalloc.ResourceAllocator().get_costs(instances, 2, 12)
$ Above function expects 12 cpu for 2 hours
```

### Version
0.1
