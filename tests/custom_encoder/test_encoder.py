import os
import time

import chaospy as cp
import easyvvuq as uq
import eqi

from eqi import TaskRequirements, Resources
from eqi import Task, TaskType, ProcessingScheme

from custom_encoder import CustomEncoder

# author: Jalal Lakhlili / Bartosz Bosak
__license__ = "LGPL"

jobdir = os.getcwd()

TEMPLATE = "tests/app_cooling/cooling.template"
APPLICATION = "tests/app_cooling/cooling_model.py"
ENCODED_FILENAME = "cooling_in.json"


def test_cooling_pj(tmpdir):
    tmpdir = str(tmpdir)

    print("Job directory: " + jobdir)
    print("Temporary directory: " + tmpdir)

    # ---- CAMPAIGN INITIALISATION ---
    print("Initializing Campaign")
    # Set up a fresh campaign called "cooling"
    my_campaign = uq.Campaign(name='cooling', work_dir=tmpdir)

    # Define parameter space
    params = {
        "temp_init": {
            "type": "float",
            "min": 0.0,
            "max": 100.0,
            "default": 95.0},
        "kappa": {
            "type": "float",
            "min": 0.0,
            "max": 0.1,
            "default": 0.025},
        "t_env": {
            "type": "float",
            "min": 0.0,
            "max": 40.0,
            "default": 15.0},
        "out_file": {
            "type": "string",
            "default": "output.csv"}}

    output_filename = params["out_file"]["default"]
    output_columns = ["te"]

    # Create an encoder, decoder and collation element for PCE test app
    # encoder = uq.encoders.GenericEncoder(
    encoder = CustomEncoder(
        template_fname=jobdir + '/' + TEMPLATE,
        delimiter='$',
        target_filename=ENCODED_FILENAME)

    decoder = uq.decoders.SimpleCSV(target_filename=output_filename,
                                    output_columns=output_columns)

    # Add the PCE app (automatically set as current app)
    my_campaign.add_app(name="cooling",
                        params=params,
                        encoder=encoder,
                        decoder=decoder
                        )

    vary = {
        "kappa": cp.Uniform(0.025, 0.075),
        "t_env": cp.Uniform(15, 25)
    }

    # Create the sampler
    my_sampler = uq.sampling.PCESampler(vary=vary, polynomial_order=3)
    # Associate the sampler with the campaign
    my_campaign.set_sampler(my_sampler)

    # Will draw all (of the finite set of samples)
    my_campaign.draw_samples()

    print("Starting execution")
    qcgpjexec = eqi.Executor(my_campaign)
    qcgpjexec.create_manager(resources='4')

    qcgpjexec.add_task(Task(
        TaskType.ENCODING,
        TaskRequirements(cores=Resources(exact=1))
    ))

    qcgpjexec.add_task(Task(
        TaskType.EXECUTION,
        TaskRequirements(cores=Resources(exact=1)),
        application='python3 ' + jobdir + "/" + APPLICATION + " " + ENCODED_FILENAME
    ))

    # qcgpjexec.add_task(Task(
    #     TaskType.ENCODING_AND_EXECUTION,
    #     TaskRequirements(cores=Resources(exact=1)),
    #     application='python3 ' + jobdir + "/" + APPLICATION + " " + ENCODED_FILENAME
    # ))

    qcgpjexec.run(processing_scheme=ProcessingScheme.SAMPLE_ORIENTED)
    qcgpjexec.terminate_manager()

    print("Collating results")
    my_campaign.collate()

    print("Making analysis")
    pce_analysis = uq.analysis.PCEAnalysis(sampler=my_sampler,
                                           qoi_cols=output_columns)
    my_campaign.apply_analysis(pce_analysis)

    results = my_campaign.get_last_analysis()

    stats = results.describe()['te'].loc['mean'], results.describe()['te'].loc['std']

    print("Processing completed")
    return stats


if __name__ == "__main__":
    start_time = time.time()

    stats = test_cooling_pj()

    end_time = time.time()
    print('>>>>> elapsed time = ', end_time - start_time)
