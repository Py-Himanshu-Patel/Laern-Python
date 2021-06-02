# Proxy Pattern

**Classification**: Structural
It acts on a real subject and keeps a reference to the subject. Proxy exposes a identical interface as original subject thus make client almost unaware of that he is using a proxy as same time controlling access to a real subject.

It stands as an interface in between client code and the actual code a client want to access. It’s recommended when you want to add some additional behaviors to an object of some existing class without changing the client code. The meaning of word **Proxy** is ___in place of___ or ___on behalf of___ that directly explains the Proxy Method. Proxy pattern controls and manage access to the object they are protecting.

- **Virtual Proxy**: A virtual proxy is a placeholder for "expensive to create" objects. The real object is only created (on demand) when a client first requests/accesses the object.
- **Protective Proxy**: A protective proxy controls access to a sensitive master object. The "surrogate" object checks that the caller has the access permissions required prior to forwarding the request.
- **Remote Proxy**: It is particularly used when the service object is located on a remote server. In such cases, the proxy passes the client request over the network handling all the details while actual resource is behind some firewall.
- **Smart proxy**: A smart proxy interposes additional actions when an object is accessed. Typical uses include:
  - Counting the number of references to the real object so that it can be freed automatically when there are no more references (aka smart pointer),
  - Loading a persistent object into memory when it's first referenced,
  - Checking that the real object is locked before it is accessed to ensure that no other object can change it.

DBMS use all of them.

## Without using Proxy

Employee Class: Resource for which we need proxy

```python
class Employee:
    def __init__(self, empid, name, birthdate, salary):
        self.empid = empid
        self.name = name
        self.birthdate = birthdate
        self.salary = salary
```

Access Control Class before retriving Employee data

```python
class AccessControl:
    def __init__(self, empid, can_see_personal):
        self.empid = empid
        self.can_see_personal = can_see_personal
```

After creating some testdata (substitute of DB) we can write a logic to let only autorized person access the sensitive info.

```python
from testdata import EMPLOYEES, ACCESSCONTROL


def get_employee_info(empids, reqid):
    for empid in empids:
        if empid not in EMPLOYEES:
            continue
        employee = EMPLOYEES[empid]
        details = 'Employee Id: %d, Name: %s'
        details = details % (employee.empid, employee.name)

        if reqid in ACCESSCONTROL:
            if ACCESSCONTROL[reqid].can_see_personal:
                details += (', BirthDate: %s, Salary: %.2f' %
                            (employee.birthdate, employee.salary))
        print(details)


get_employee_info([3, 4], 3)  # requestor may not see personal data

get_employee_info([1, 2], 101)  # requestor *may* see personal data
```

## Proxy Pattern Structure

- **Abstract Subject**: Subject class is a abstract class which defines the interfaces client is expected to use while interacting with it.
- **Concrete Subject**: Concrete class which implement the abstract method and properties declared in abstract subject.
- **Proxy**: It containt reference to original concrete class so as to preoduce the actual object for valid request. And also contains same interface as declared in abstract subject so as to provide same interface for client while using proxy. Client request is received by client and client do not know about any proxy and directly make requrest as if it is making request directly with Subject.

