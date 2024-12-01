# Currency Converter for the Rest of Us

A **_simple_** Alfred 4 currency converter tailored to **_your_** needs.

Show the currencies you care at light speed. No API key required.

This workflow targets simplicity at the cost of preciseness.
My goal is to cover the most common use cases in daily life: **_at a glance_**, get a rough conversion between the currencies **_I care about_**.

Before writing this workflow, this is typically done by googling `100 CHF to USD`, which is lighting fast already.
If the workflow cannot make things even simpler (e.g. the need to register/renew API keys, the cost to remember commands, and the waiting time), the workflow is useless.

This workflow uses the [European Central Bank Feed](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html#dev) as the data source and relies on the exchange rates being (mostly) _**transitive**_ (A to B ≈ A to C to B).
It's not very timely (data is updated every working day).
It's not very comprehensive (only a few common currencies are covered).
It's not very accurate (rates are not completely transitive).
But in the cases I need timeliness, comprehensiveness, and/or accuracy, I can always fall back to googling `100 CHF to USD`.

![](preview.gif)

## Setup
Download the latest version at [releases](https://github.com/liuzikai/alfred-currency-converter-for-the-rest-of-us/releases).

Python dependency `requests` is needed. The installation command can be like:
```shell
pip3 install requests
```
Note that Alfred may use the OS built-in Python by default (rather than ones from e.g. HomeBrew). In this case, you may want to use `/usr/bin/pip3` or change `python3` in the script filters to another Python executable.

## Configure for your needs
Open the workflow configuration.

Every script filter is a base currency. In its setting, the script specify the conversion. 

For example,
```
python3 convert.py 'CHF' 'CNY,EUR,USD,JPY' {query}
```
means the base currency is CHF and the target currencies are CNY, EUR, USD, and JPY.

To create a new base currency (trigger), simply copy and paste one script filter, change the script and connect it to the conditional block.
