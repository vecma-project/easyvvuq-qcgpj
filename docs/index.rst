.. EasyVVUQ-QCGPJ documentation master file, created by
   sphinx-quickstart on Wed May 20 12:51:45 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EasyVVUQ-QCGPJ - Python API for HPC execution of EasyVVUQ!
==========================================================

EasyVVUQ-QCGPJ is a lightweight plugin for parallelization of EasyVVUQ (https://github.com/UCL-CCS/EasyVVUQ)
with the QCG Pilot Job system (https://github.com/vecma-project/QCG-PilotJob).

It is developed as part of VECMA (http://www.vecma.eu), and is part of the VECMA Toolkit (http://www.vecma-toolkit.eu).

The tool provides API that can be effortlessly integrated into typical EasyVVUQ workflows to enable parallel processing
of demanding operations, in particular the simulation model's executions and encodings.
It works regardless if you run your use-case on multi-core laptop or on large HPC machine.

You can start using it whenever you want: from the beginning of your work with EasyVVUQ or
once you realise that the serial execution of EasyVVUQ is no longer sufficient.

In the rest of this documentation EasyVVUQ-QCGPJ is shortened as EasyPJ and QCG Pilot Job as QCG PJ


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   quickstart
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`