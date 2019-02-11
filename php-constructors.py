import sublime
import sublime_plugin
import re
from os.path import dirname, realpath

def echo(msg):
	print ("[PHP Constructors] %s" % msg)

class PhpGenerateConstructorCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# TODO: Verify if constructor already exists and skip

		# Load settings for future usage
		settings = sublime.load_settings('PHP Constructors.sublime-settings')
		setting_optional_params = settings.get('optional_constructor_params')
		setting_ignore_visibility = settings.get('ignore_visibility_notation')
		setting_pass_array = settings.get('parameter_as_array')

		# Get regions of the class attributes
		classAttributes = self.getClassAttributeRegions()

		# Get list with attr names
		attributes = self.getAttributeNamesList(classAttributes)

		# Get documentation block content
		docblock = self.getDockblock(attributes, setting_ignore_visibility, setting_pass_array)

		# Get internal content for constructor
		internalConstructorContent = self.getInternalConstructorContent(attributes, setting_ignore_visibility, setting_pass_array)

		# Get parameter list for constructor
		parameterList = self.getParameterList(attributes, setting_optional_params, setting_ignore_visibility, setting_pass_array)

		# Get complete contents of the constructor
		constructor = self.getConstructor(docblock, parameterList, internalConstructorContent)

		# Get the position to insert the constructor
		insertPosition = self.getConstructorPosition(classAttributes)

		# Insert constructor
		if insertPosition == None or insertPosition == -1:
			# echo('Couldn\'t insert constructor in file:' + self.view.file_name())
			echo('Can\'t insert constructor here.')
		else:
			self.view.insert(edit, insertPosition, constructor)

	def getTemplate(self, templateName):
		template = ''

		if templateName == 'constructor':
			template = '''
:docblock
	public function __construct(:parameter_list)
	{
		:attribute_setters
	}
'''

		return template
		# return open(dirname(realpath(__file__)) + '/templates/' + templateName).read()

	def getClassAttributeRegions(self):
		# Search attributes in the current view
		attributeLineRegex = '((?:private|public|protected)[ ]{0,}(?:final|static)?[ ]{0,}(?:\$.*?)[ |=|;].*)\n'
		return self.view.find_all(attributeLineRegex, sublime.IGNORECASE)

	def getAttributeNamesList(self, classAttributeRegions):
		# Iterate over the attribute matches and get the content for each one
		attributeNameRegex = '\s(\$\w+)'
		attributes = []

		for attribute in classAttributeRegions:
			attrContent = self.view.substr(attribute);
			variableName = re.search(attributeNameRegex, attrContent, re.IGNORECASE).group(1)
			attributes.append(variableName)

		return attributes

	def getDockblock(self, attributeNamesList, ignoreVisibility, passArray):
		viewContent = self.view.substr(sublime.Region(0, self.view.size()))
		# docRegex = '/\*\*\n\s*\*\s+@var\s+([\w\\\\]+) (.*)\n\s*.*\*/\n\s*.*\$'
		docBothRegex = '/\*\*\n\s*\*\s+(.*)\n\s*\*\s+@var\s+([\w\\\\]+).*\n\s*\*\/\n\s*.*\$'
		docVarRegex = '/\*\*\n\s*\*\s+@var\s+([\w\\\\]+).*\n\s*\*\/\n\s*.*\$'
		docDescRegex = '/\*\*\n\s*\*\s+(.*)\n\s*\*\/\n\s*.*\$'

		docblockTemplate = '	/**\n	 * Class Constructor:param_list\n	 */\n'
		parameters = ''

		if passArray == True:
			parameters = '\n	 * @param array $data\n'
		else:
			if len(attributeNamesList) > 0:
				parameters += '\n'

			for attribute in attributeNamesList:
				paramType = ''
				paramDescription = ''

				matches = re.search(docBothRegex + attribute[1:], viewContent, re.IGNORECASE)
				if matches == None:
					matches = re.search(docVarRegex + attribute[1:], viewContent, re.IGNORECASE)
					if matches == None:
						matches = re.search(docDescRegex + attribute[1:], viewContent, re.IGNORECASE)
						if matches != None:
							paramDescription = matches.group(1)
					else:
						paramType = matches.group(1)
				else:
					paramType = matches.group(2)
					paramDescription = matches.group(1)


				if ignoreVisibility == True and attribute[1] == '_':
					attribute = '$' + attribute[2:]

				parameter = '	 * @param ' + attribute

				if paramType != '':
					parameter += ('  ' + paramType)

				if paramDescription != '':
					parameter += ('  (' + paramDescription + ')')

				parameter += '\n'

				parameters += parameter

		return docblockTemplate.replace(':param_list', parameters[:-1])[:-1]

	def getInternalConstructorContent(self, attributeNamesList, ignoreVisibility, passArray):
		# Build the internal part of the constructor
		internalConstructorContent = ''

		for variableName in attributeNamesList:
			parameterName = variableName

			if ignoreVisibility == True and parameterName[1] == '_':
				parameterName = '$' + parameterName[2:]

			if passArray == True:
				parameterName = '$data[\'' + parameterName[1:] + '\']'

			internalConstructorContent += '\t\t$this->' + variableName[1:] + ' = ' + parameterName + ';\n'

		return internalConstructorContent[2:-1]

	def getParameterList(self, attributeNamesList, optionalParams, ignoreVisibility, passArray):
		# Join the attributes to add it as a parameter list for the constructor
		if passArray == True:
			parameterList = 'array $data'
		else:
			if ignoreVisibility == True:
				for i, attribute in enumerate(attributeNamesList):
					if attributeNamesList[i][1] == '_':
						attributeNamesList[i] = '$' + attribute[2:]

			if optionalParams == True:
				parameterList = ' = null, '.join(attributeNamesList) + ' = null'
			else:
				parameterList = ', '.join(attributeNamesList)

		return parameterList

	def getConstructor(self, docblock, parameters, internalConstructorContent):
		constructorTemplate = self.getTemplate('constructor')

		# Replace tokens in template with actual data
		constructor = constructorTemplate.replace(':docblock', docblock)
		constructor = constructor.replace(':parameter_list', parameters)
		constructor = constructor.replace(':attribute_setters', internalConstructorContent)

		return constructor

	def getConstructorPosition(self, classAttributesRegions):
		position = None

		if len(classAttributesRegions) == 0:
			position = self.view.find('class\s+\w[\w\s\n]+\{', sublime.IGNORECASE).end()
		else:
			position = classAttributesRegions[-1].end()

		return position
