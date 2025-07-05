# Attack Phase

## Dialogue template
All the dialogue scene templates used for the experiment are in scenario_template.py.

## Jailbreak dialogue generation

**attack_data_generation.py**

Obtain the corresponding template from the specified dialogue scene to generate the induction dialogue.

Specify the format for the model to generate responses:

    "Please provide exactly 5 key points in the format of a 1-5 point reference plan, without any additional explanation or sentences."

## Multiple rounds of jailbreak attacks

**multi_round_dialogue.py**

For all the collected models, based on the sensitive issues in harmful_dict.txt, the generated dialogue is used to induce the models, and the responses of the models are saved to the file for subsequent processing.

**Save format:**

    {
        "Scenario Template 1":" Model Response"
        "Scenario Template 1":" Model Response"
        ... ...
    }


## Sensitive Issues Dictionary

**harmful_dict.txt**

It has saved a variety of sensitive topics under different categories. Under normal circumstances, the model will refuse to answer related questions involving these.

## Processing of model output results

### utils/

