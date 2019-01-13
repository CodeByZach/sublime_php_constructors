#PHP Constructors

PHP Constructors generates for you PHP Classes constructors.

##Features:
* Generate class constructor
* Description, type and var name automatically discovered from the variable docblock.

##Usage Instruction:
1. Write your class properties inside your PHP class:

```
class test
{
	/**
	 * @var my\long\namespace Var that holds foo
	 */
	private $foo;
}
```

2. Go to _Tools > Packages > PHP Constructors_
3. Select _Generate PHP Constructor for Class_

```
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

Take some time to document your class properties with in following format:

```
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

* Generate PHP Constructor for Class

This command can be accessed via the _Tools > Packages > PHP Constructors_ or via the Command Palette.

##Available Settings

####optional_constructor_params
_type_   : **boolean**

_default_: **false**

_description_: If set to true, constructors will be generated with optional parameters.

####ignore_visibility_notation
_type_   : **boolean**

_default_: **false**

_description_: If set to true, will omit underscore on private variables for constructor parameters.

####parameter_as_array
_type_   : **boolean**

_default_: **false**

_description_: If set to true, will pass all parameters to the constructor in a single array.
