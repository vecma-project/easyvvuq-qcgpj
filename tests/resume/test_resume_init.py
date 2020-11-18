import os
import time

import chaospy as cp
import easyvvuq as uq

import eqi

# author: Jalal Lakhlili / Bartosz Bosak
__license__ = "LGPL"


TEMPLATE = "tests/APP_COOLING/cooling.template"
APPLICATION = "tests/APP_COOLING/cooling_model.py"
ENCODED_FILENAME = "cooling_in.json"

if "SCRATCH" in os.environ:
    tmpdir = os.environ["SCRATCH"]
else:
    tmpdir = "/tmp/"

jobdir = os.getcwd()


def test_cooling_pj():
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
    output_columns = ["te", "ti"]

    # Create an encoder, decoder and collation element
    encoder = uq.encoders.GenericEncoder(
        template_fname=jobdir + '/' + TEMPLATE,
        delimiter='$',
        target_filename=ENCODED_FILENAME)

    decoder = uq.decoders.SimpleCSV(target_filename=output_filename,
                                    output_columns=output_columns,
                                    header=0)

    collater = uq.collate.AggregateSamples(average=False)

    # Add the PCE app (automatically set as current app)
    my_campaign.add_app(name="cooling",
                        params=params,
                        encoder=encoder,
                        decoder=decoder,
                        collater=collater
                        )

    vary = {
        "kappa": cp.Uniform(0.025, 0.075),
        "t_env": cp.Uniform(15, 25)
    }

    # Create the sampler
    my_sampler = uq.sampling.QMCSampler(vary=vary, n_mc_samples=5)

    # Associate the sampler with the campaign
    my_campaign.set_sampler(my_sampler)

    # Will draw all (of the finite set of samples)
    my_campaign.draw_samples()

    # Safe state of a campaign to state_file
    my_campaign.save_state(my_campaign.campaign_dir + "/state_before_eqi")

    print("Starting execution")
    qcgpjexec = eqi.Executor(my_campaign)

    # Create QCG PJ-Manager with 4 cores
    # (if you want to use all available resources remove resources parameter)
    qcgpjexec.create_manager(resources="4", log_level='debug')

    qcgpjexec.add_task(eqi.Task(
        eqi.TaskType.ENCODING,
        eqi.TaskRequirements(cores=1)
    ))

    qcgpjexec.add_task(eqi.Task(
        eqi.TaskType.EXECUTION,
        eqi.TaskRequirements(cores=1),
        application='python3 ' + jobdir + "/" + APPLICATION + " " + ENCODED_FILENAME
    ))

    qcgpjexec.run(submit_order=eqi.SubmitOrder.RUN_ORIENTED)

    qcgpjexec.terminate_manager()

    print("Collating results")
    my_campaign.collate()

    print("Making analysis")

    analysis = uq.analysis.QMCAnalysis(sampler=my_sampler, qoi_cols=output_columns)

    my_campaign.apply_analysis(analysis)

    results = my_campaign.get_last_analysis()
    stats = results.describe()['te']['mean'], results.describe()['te']['std']

    print("Processing completed")
    return stats


if __name__ == "__main__":
    start_time = time.time()

    stats = test_cooling_pj()
    print(stats)

    end_time = time.time()
    print('>>>>> elapsed time = ', end_time - start_time)
