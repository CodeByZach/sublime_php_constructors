import sublime
import sublime_plugin
import os


class ZEditSettings(sublime_plugin.WindowCommand):
	def run(self, **kwargs):
		is_parent_setting = False

		if 'is_parent_setting' in kwargs:
			is_parent_setting = kwargs.get('is_parent_setting')
			del kwargs['is_parent_setting']

		if is_parent_setting:
			expanded_target_directory = sublime.expand_variables(os.path.dirname(kwargs.get('file')), self.window.extract_variables())
			if not os.path.exists(expanded_target_directory):
				os.makedirs(expanded_target_directory)

			if 'contents' in kwargs:
				kwargs['contents'] = kwargs.get('contents')

			self.window.run_command('open_file', kwargs)

		else:
			if 'user_file' in kwargs:
				expanded_target_directory = sublime.expand_variables(os.path.dirname(kwargs.get('user_file')), self.window.extract_variables())
				if not os.path.exists(expanded_target_directory):
					os.makedirs(expanded_target_directory)

			try:
				expanded_source_path = sublime.expand_variables(kwargs.get('base_file'), self.window.extract_variables())
				# package_name = os.path.basename(os.path.dirname(expanded_source_path.replace(sublime.packages_path(), '')))
				resource_path = 'Packages'+expanded_source_path.replace(sublime.packages_path(), '')
				sublime.load_resource(resource_path)

				self.window.run_command('edit_settings', kwargs)
			except IOError:
				if 'user_file' in kwargs:
					kwargs['file'] = kwargs.get('user_file')
					del kwargs['user_file']
				else:
					# expanded_source_path = sublime.expand_variables(kwargs.get('base_file'), self.window.extract_variables())
					# kwargs['file'] = expanded_source_path.replace(sublime.packages_path(), os.path.join(sublime.packages_path(), 'User'))
					kwargs['file'] = os.path.join(sublime.packages_path(), 'User', os.path.basename(kwargs.get('base_file')))
				del kwargs['base_file']
				kwargs['contents'] = kwargs.get('default')
				del kwargs['default']

				self.window.run_command('open_file', kwargs)
