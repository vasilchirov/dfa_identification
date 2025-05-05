import subprocess
import sys
import graphviz


def flexfringe(*args, **kwargs):
    """Wrapper to call the flexfringe binary

     Keyword arguments:
     position 0 -- input file with trace samples (from flexfringe build)
     position 1 -- location of the FlexFringe build directory (e.g. ../Flexfringe/build/)
     kwargs -- list of key=value arguments to pass as command line arguments
    """
    command = ["--help"]

    if len(kwargs) >= 1:
        command = []
        for key in kwargs:
            command += ["--" + key + "=" + kwargs[key]]

    result = subprocess.run(["./flexfringe", ] + command + [args[0]], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True, cwd=args[1])
    print(result.returncode, result.stdout, result.stderr)

    try:
        with open(args[1] + args[0] + ".ff.final.dot") as fh:
            return fh.read()
    except FileNotFoundError:
        pass

    return None


def show(data, filename="output_DFA"):
    """Save a .png representation of the graph in output_DFAs/

      Keyword arguments:
      data -- string formated in graphviz dot language to visualize
      filename -- output file name
    """
    if not data:
        pass
    else:
        g = graphviz.Source(data, format="png")
        g.render("output_DFAs/" + filename, cleanup=True)
