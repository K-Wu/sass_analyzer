# -*- coding: utf-8 -*-

from io import StringIO

from sass_analyzer.CuAssembler.CuInsFeeder import CuInsFeeder, SLT


class MyCuInsFeeder(CuInsFeeder):
    def extract_all(self, fout, *, func_filter=None, ins_filter=None):
        """Extracting kernel matching the filter to fout.
        2-line modified function based on the original extract()

        Sometimes whole kernel sass is needed to check the context of an instruction,
        this will help to identify some rules of instruction correlations.

            fout: output filename
            func_filter: filter for the function name, may be string/re.Pattern/callable
            ins_filter: filter for the instruction

        Match rules:
            1. when func_filter matched the name, output *ALL* matched kernel;
            2. when ins_filter matched an instruction, output the first kernel containing the instruction;
        """
        buf = StringIO()
        do_dump = False

        InsFilterFun = CuInsFeeder.parseInsFilter(ins_filter)
        FuncFilterFun = CuInsFeeder.parseInsFilter(func_filter)

        def tryDump():
            if do_dump:
                if buf.tell() == 0:
                    print("Empty buffer! Nothing to dump...")
                    return False

                print("================================")
                print(buf.getvalue())
                with open(fout, "a") as fout_stream:
                    print(f"Dump to file {fout}...")
                    fout_stream.write(buf.getvalue())
                return True
            else:
                return False

        while True:
            linetype, line, res = self.nextParseLine()

            if linetype is None:
                tryDump()
                break

            if linetype == SLT.FuncName:
                tryDump()
                # We remove the if True then break here to dump all functions
                if func_filter is not None:
                    if FuncFilterFun(res.group("func")):
                        do_dump = True
                buf = StringIO()
            elif linetype in {SLT.InsCode, SLT.InsOnly, SLT.CodeOnly}:
                if InsFilterFun(line):
                    do_dump = True
            else:
                pass

            buf.write(line.rstrip() + "\n")

        if not do_dump:
            print("Nothing to dump...")


if __name__ == "__main__":
    feeder = MyCuInsFeeder("sass_analyzer/test/export_op.dump.sass")
    feeder.extract_all("sass_analyzer/test/export_op.dump.sass.out")
