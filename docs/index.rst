.. EasyVVUQ-QCGPJ documentation master file, created by
   sphinx-quickstart on Wed May 20 12:51:45 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EasyVVUQ-QCGPJ
==============
**Python API for HPC execution of EasyVVUQ**

EasyVVUQ-QCGPJ (EQI) is a lightweight
plugin for parallelization of `EasyVVUQ <https://github.com/UCL-CCS/EasyVVUQ>`_
with the `QCG-PilotJob <https://github.com/vecma-project/QCG-PilotJob>`_

It is a part of the `VECMA Toolkit <http://www.vecma-toolkit.eu>`_

The tool provides API that can be effortlessly integrated into typical EasyVVUQ workflows
to enable parallel processing of demanding operations on HPC machines.

It can work also on your laptop so you can start using it whenever you want:
from the beginning of your work with EasyVVUQ or once you realise that
the serial execution of EasyVVUQ is no longer sufficient.


.. toctree::
   :caption: Basics

   installation
   quickstart
   api

.. toctree::
   :caption: Further reading

   performance_optimisation

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorials/cooling_cup/guide/tutorial
   tutorials/interactive_tutorial

.. toctree::
   :maxdepth: 1
   :caption: API Docs

   api/eqi

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

Authors
-------
| Bartosz Bosak <bbosak@man.poznan.pl> (PSNC)
| Piotr Kopta <pkopta@man.poznan.pl> (PSNC)
| Tomasz Piontek <pkopta@man.poznan.pl> (PSNC)
| Jalal Lakhlili <jalal.lakhlili@ipp.mpg.de> (IPP)
