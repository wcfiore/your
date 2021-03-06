import glob
import os
import shutil

from keras_autodoc import DocumentationGenerator

pages = {
    'your.md': ["your.Your",
                "your.Your.bandpass",
                "your.Your.get_data",
                "your.Your.dispersion_delay",
                "your.Header"],

    'candidate.md': ["your.candidate.Candidate",
                     "your.candidate.Candidate.save_h5",
                     "your.candidate.Candidate.dispersion_delay",
                     "your.candidate.Candidate.get_chunk",
                     "your.candidate.Candidate.dedisperse",
                     "your.candidate.Candidate.dedispersets",
                     "your.candidate.Candidate.dmtime",
                     "your.candidate.Candidate.get_snr",
                     "your.candidate.Candidate.optimize_dm",
                     "your.candidate.Candidate.decimate",
                     "your.candidate.Candidate.resize"],

    'writer.md': ['your.writer.Writer.to_fil',
                     'your.writer.Writer.to_fits'],

    'formats/psrdada.md': ['your.formats.dada.DadaManager',
                      'your.formats.dada.DadaManager.setup',
                      'your.formats.dada.DadaManager.dump_header',
                      'your.formats.dada.DadaManager.dump_data',
                      'your.formats.dada.DadaManager.mark_filled',
                      'your.formats.dada.DadaManager.eod',
                      'your.formats.dada.DadaManager.teardown',
                      'your.formats.dada.YourDada',
                      'your.formats.dada.YourDada.setup',
                      'your.formats.dada.YourDada.teardown',
                      'your.formats.dada.YourDada.your_dada_header',
                      'your.formats.dada.YourDada.to_dada'],

    'formats/pysigproc.md': ['your.formats.pysigproc.SigprocFile',
                        'your.formats.pysigproc.SigprocFile.get_data',
                        'your.formats.pysigproc.SigprocFile.unpack',
                        'your.formats.pysigproc.SigprocFile.write_header',
                        'your.formats.pysigproc.SigprocFile.append_spectra'],

    'formats/psrfits.md': ['your.formats.psrfits.PsrfitsFile',
                      'your.formats.psrfits.PsrfitsFile.read_subint',
                      'your.formats.psrfits.PsrfitsFile.get_data',
                      'your.formats.psrfits.SpectraInfo',
                      'your.formats.psrfits.unpack_2bit',
                      'your.formats.psrfits.unpack_2bit',                      
                      'your.formats.psrfits.unpack_4bit'],

    'formats/filwriter.md': ["your.formats.filwriter.make_sigproc_obj",
                        "your.formats.filwriter.write_fil"],

    'formats/fitswriter.md': ["your.formats.fitswriter.initialize_psrfits",
                         "your.formats.fitswriter.ObsInfo"],

    'utils/rfi.md': ["your.utils.rfi.savgol_filter",
                     "your.utils.rfi.spectral_kurtosis"],

    'utils/plotter.md': ["your.utils.plotter.figsize",
                         "your.utils.plotter.get_params",
                         "your.utils.plotter.plot_h5",
                         "your.utils.plotter.save_bandpass"],

    'utils/astro.md': ["your.utils.astro.dec2deg",
                       "your.utils.astro.ra2deg"],

    'utils/heimdall.md': ["your.utils.heimdall.HeimdallManager",
                          "your.utils.heimdall.HeimdallManager.run"],

    'utils/math.md': ["your.utils.math.closest_number",
                      "your.utils.math.primes",
                      "your.utils.math.closest_divisor",
                      "your.utils.math.find_gcd",
                      "your.utils.math.normalise",
                      "your.utils.math.smad_plotter"],

    'utils/gpu.md': ["your.utils.gpu.gpu_dedisperse",
                     "your.utils.gpu.gpu_dmt",
                     "your.utils.gpu.gpu_dedisp_and_dmt_crop",
                     "your.utils.gpu.get_gpu_memory_map"],

    'utils/misc.md': ["your.utils.misc.crop",
                      "your.utils.misc.pad_along_axis",
                      "your.utils.misc.MyEncoder"],

}

doc_generator = DocumentationGenerator(pages)
doc_generator.generate('./sources')

shutil.copyfile('../README.md', 'sources/index.md')

os.system("mkdir -p sources/bin")

for bin_files in glob.glob("../bin/*py"):
    output_file = "sources/bin/" + os.path.basename(bin_files)[:-2] + 'md'
    os.system(f"argdown --tiny -o {output_file} {bin_files}")

github_repo_dir = 'devanshkv/your/blob/master/examples/'

for ipynb_files in glob.glob("../examples/*ipynb"):
    os.system(f"jupyter-nbconvert {ipynb_files} --to markdown --output-dir=sources/ipynb/")
    file_name_no_ext = ipynb_files.split("/")[-1][:-6]
    md_path = f"sources/ipynb/{file_name_no_ext}.md"
    with open(md_path, 'r') as md_file:
        button_lines = [
            ':material-link: '
            "[**View in Colab**](https://colab.research.google.com/github/"
            + github_repo_dir
            + file_name_no_ext + ".ipynb"
            + ")   &nbsp; &nbsp;"
            # + '<span class="k-dot">•</span>'
            + ':octicons-octoface: '
              "[**GitHub source**](https://github.com/" + github_repo_dir + file_name_no_ext + ".ipynb)",
            "\n",
        ]
        md_content = ''.join(button_lines) + '\n' + md_file.read()

    with open(md_path, 'w') as md_file:
        md_file.write(md_content)
