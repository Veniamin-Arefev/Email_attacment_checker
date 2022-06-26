"""Test module"""
from io import StringIO
import re
import unittest
from unittest.mock import patch

from netjudge.report_analyser.appcmd import import_files_from_dir
from netjudge.report_analyser.appcmd import import_instructions_from_json
from netjudge.report_analyser.appcmd import Repl


def cleanoutput(s):
    """Clean output."""
    s = re.sub('\\x1b\[\d*m', '', s)
    s = re.sub('[ \t\n]+', '', s)
    return s


class AppCmdTest(unittest.TestCase):
    """Class for tests."""

    def test_import_files_from_dir(self):
        """Import tests from dir."""
        output = """Success
input_example/veniamin   report.03.base
input_example/veniamin   report.03.bridge
input_example/dima   report.03.base
input_example/dima   report.03.bridge
input_example/dima   report.03.clone\n"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            import_files_from_dir(['input_example/', ])
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_import_files_from_dir_nofile(self):
        """Import files that does not exist."""
        output = 'No such file or directory'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            import_files_from_dir(['nofile/', ])
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_instructions_from_json(self):
        """Import json instructions."""
        output = '''Success\n
 Re: 10.10.10.\d
   Files (input):\treport.03.clone
 Re: Script started on
   Every imported file (output).
 Re: vlan7
   Files (input):\treport.03.base report.03.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            import_instructions_from_json(['input_example/instruction.json', ])
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_instructions_from_json_nofile(self):
        """Import non-existing instructions."""
        output = '''[Errno 2] Nosuchfileordirectory: 'input_example/nofile.json'\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            import_instructions_from_json(['input_example/nofile.json', ])
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_EOF(self):
        """Quit test."""
        output = '''==[Exiting!]==\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_EOF('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_exit(self):
        """Exit test."""
        output = '''==[Exiting!]==\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_exit('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_reset(self):
        """Reset test."""
        output = ''' ==[ All progress is reset!! ]==\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_importedreports_nofile(self):
        """No reports imported test."""
        output = '''  =[ No reports imported ]=\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_importedreports('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_importedreports(self):
        """Import test."""
        output = '''  =[ Imported reports: ]=
Participant: input_example/veniamin His files:
        report.03.base   report.03.bridge        
Participant: input_example/dima His files:
        report.03.base   report.03.bridge        report.03.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            import_files_from_dir(['input_example/', ])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_importedreports('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_importedinstructions_nofile(self):
        """No import file test."""
        output = ''' =[No instructions imported]=\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_importedinstructions('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_importedinstructions(self):
        """Instruction test."""
        output = '''=[ Imported instructions: ]=
 Re: 10.10.10.\d
   Files (input):       report.03.clone
 Re: Script started on
   Every imported file (output).
 Re: vlan7
   Files (input):       report.03.base  report.03.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            import_instructions_from_json(['input_example/instruction.json', ])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_importedinstructions('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addrep(self):
        """Adding repository test."""
        output = '''Success
input_example/veniamin   report.03.base
input_example/veniamin   report.03.bridge
input_example/dima   report.03.base
input_example/dima   report.03.bridge
input_example/dima   report.03.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addrep('input_example/')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addrep_nofile(self):
        """Repository does not exist test."""
        output = 'No such file or directory'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addrep('nofile/')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addins(self):
        """Add instructions test."""
        output = '''Success\n
 Re: 10.10.10.\d
   Files (input):\treport.03.clone
 Re: Script started on
   Every imported file (output).
 Re: vlan7
   Files (input):\treport.03.base report.03.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addins('input_example/instruction.json')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addins_nofile(self):
        """No instruction file test."""
        output = '''[Errno 2] Nosuchfileordirectory: 'input_example/nofile.json'\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addins('input_example/nofile.json')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addreg(self):
        """Add regex test."""
        output = '''Success\n
 Re: 20.20.20.
   Files (output):\treport.06.clone\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addreg('20.20.20. out report.06.clone')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_addreg_2(self):
        """Another add regex test."""
        output = '''Success\n
 Re: 20.20.20.
   Every imported file (output).\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_addreg('20.20.20. out')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_help_start(self):
        """Start test."""
        output = '''Main function to start checking process. Checking steps:

        Usage: start ['1'/'2']

        1. Parsing & Syntax check;
        2. Parsing & Syntax check & Semantic check.

        No files in collection:              # # steps done
        Files present in collection:         1 # steps done
        Instructions present in collection:  1 2 steps done

        Results are saved and can be shown with 'conclude'.\n'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_help('start')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_start_1(self):
        """Start 1 test."""
        output = """No instructions imported! => Second step is skipped
Use 'addins INSTRUCTION_FILE'
Or  'addreg REGEX, FILE1, FILE2...'
  ==[ CHECK STARTS:  Going through 1 steps ]==
  =[ SYNTAX CHECK ]=
Participant: ' input_example/veniamin ', his files:
         input_example/veniamin/report.03.base
         input_example/veniamin/report.03.bridge
Participant: ' input_example/dima ', his files:
         input_example/dima/report.03.base
         input_example/dima/report.03.bridge
         input_example/dima/report.03.clone
  ==[ CHECK ENDED ]==\n"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            import_files_from_dir(['input_example/', ])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_start('1')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_start_2(self):
        """Start 2 test."""
        output = """==[ CHECK STARTS:  Going through 2 steps ]==
  =[ SYNTAX CHECK ]=
Participant: ' input_example/veniamin ', his files:
         input_example/veniamin/report.03.base
         input_example/veniamin/report.03.bridge
Participant: ' input_example/dima ', his files:
         input_example/dima/report.03.base
         input_example/dima/report.03.bridge
         input_example/dima/report.03.clone
  =[ SEMANTIC CHECK ]=
Checking participant 'input_example/veniamin':

  Checking file report.03.base:
    RE 0: 'Script started on' (output).
      Match 1 in line 0:
        Script started on 2022-03-11 10:08:28+00:00 [TERM="linux" TTY="/dev/tty1" COLUMNS="100" LINES="37"]
  1 / 1 REGEXs matched in file report.03.base

    RE 1: 'vlan7' (input).
      Match 1 in line 1:
        ip link add link eth1 name vlan7 type vlan id 7
      Match 2 in line 2:
        ip address add dev vlan7 10.10.10.7/24
  1 / 1 REGEXs matched in file report.03.base


  Checking file report.03.bridge:
    RE 0: 'Script started on' (output).
      Match 1 in line 0:
        Script started on 2022-03-11 10:07:38+00:00 [TERM="linux" TTY="/dev/tty1" COLUMNS="100" LINES="37"]
  1 / 1 REGEXs matched in file report.03.bridge

Checking participant 'input_example/dima':

  Checking file report.03.base:
    RE 0: 'Script started on' (output).
      Match 1 in line 0:
        Script started on 2022-03-11 10:08:28+00:00 [TERM="linux" TTY="/dev/tty1" COLUMNS="100" LINES="37"]
  1 / 1 REGEXs matched in file report.03.base

    RE 1: 'vlan7' (input).
      Match 1 in line 1:
        ip link add link eth1 name vlan7 type vlan id 7
      Match 2 in line 2:
        ip address add dev vlan7 10.10.10.7/24
  1 / 1 REGEXs matched in file report.03.base


  Checking file report.03.bridge:
    RE 0: 'Script started on' (output).
      Match 1 in line 0:
        Script started on 2022-03-11 10:07:38+00:00 [TERM="linux" TTY="/dev/tty1" COLUMNS="100" LINES="37"]
  1 / 1 REGEXs matched in file report.03.bridge


  Checking file report.03.clone:
    RE 0: '10.10.10.\d' (input).
      Match 1 in line 2:
        ip address add dev vlan9 10.10.10.9/24
      Match 2 in line 4:
        ping -c8 10.10.10.7
  1 / 1 REGEXs matched in file report.03.clone

    RE 1: 'Script started on' (output).
      Match 1 in line 0:
        Script started on 2022-03-11 10:09:09+00:00 [TERM="linux" TTY="/dev/tty1" COLUMNS="100" LINES="37"]
  1 / 1 REGEXs matched in file report.03.clone

    RE 2: 'vlan7' (input).
      No matches in 0 lines!
  0 / 1 REGEXs matched in file report.03.clone

  ==[ CHECK ENDED ]==\n"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            Repl().do_addrep('input_example/')
            Repl().do_addins('input_example/instruction.json')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_start('2')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))

    def test_do_conclude(self):
        """Start conclude test."""
        output = '''==[ RESULTS ]==
Participant 'input_example/veniamin' results:

  report.03.base:       2 / 2
  report.03.bridge:     1 / 1

Participant 'input_example/dima' results:

  report.03.base:       2 / 2
  report.03.bridge:     1 / 1
  report.03.clone:      2 / 3'''
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_reset('')
            Repl().do_addrep('input_example/')
            Repl().do_addins('input_example/instruction.json')
            Repl().do_start('2')
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Repl().do_conclude('')
            self.assertEqual(cleanoutput(fake_out.getvalue()), cleanoutput(output))


if __name__ == "__main__":
    unittest.main()
