#PHP Constructors

PHP Constructors generates for you PHP Classes constructors.

##Features:
* Generate class constructor
* Description, type and var name automatically discovered from the variable docblock.

##Usage Instruction:
1. Write your class properties inside your PHP class:

```php
class test
{
	/**
	 * @var my\long\namespace Var that holds foo
	 */
	private $foo;
}
	```

2. Go to Tools -> PHP Constructor
3. Constructor will be generated

```php
class test
{
	/**
	 * @var my\long\namespace Var that holds foo
	 */
	private $foo;

	/**
	 * Class Constructor
	 * @param my\long\namespace   $foo    Var that holds foo
	 */
	public function __construct($foo)
	{
		$this->foo = $foo;
	}
}
```

Take sometime to document your class properties with the following format:

```php
class test
{
	/**
	 * @var varType Description of the var
	 */
	private $foo;
}
```

##Commands

Commands available are:

* Generate Constructor for Class

This option can be accessed via the contextual menu (right click) or on the command palette.

##Available Settings

####optional_constructor_params
_type_   : **boolean**

_default_: **false**

_description_: If set to true generated constructor will be generated with optional parameters.
