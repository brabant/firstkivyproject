# -*- coding: utf-8 -*-

import os
import sys
import traceback

directory = os.path.split(os.path.abspath(sys.argv[0]))[0]

try:
    import kivy
    kivy.require('1.9.1')

    from kivy.app import App
    # from kivy.config import Config
    # Config.set('kivy', 'keyboard_mode', 'system')
except Exception:
    # traceback.print_exc(file=open('{}/error.log'.format(directory), 'w', encoding='utf-8'))
    text_error = traceback.format_exc()
    open('{}/error.log'.format(directory), 'w', encoding='utf-8').write(text_error)
    print(text_error)
    sys.exit(1)


__version__ = '0.0.1'


def main():
    app = None

    try:
        from program import Program  # основной класс программы

        # Запуск приложения.
        app = Program()
        app.run()
    except Exception:
        text_error = traceback.format_exc()
        open('{}/error.log'.format(directory), 'w', encoding='utf-8').write(text_error)
        print(text_error)
        sys.exit(1)


if __name__ in ('__main__', '__android__'):
    main()
