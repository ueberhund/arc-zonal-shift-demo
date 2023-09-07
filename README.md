# arc-zonal-shift-demo
A simple demo application that can be used with Route 53 Application Recovery Controller Zonal Shift

Simply deploy the CFN template. Once everything comes into service (you can view the website by looking at the CFN Outputs tab), go to the Route 53 Application Recovery Controller console and start a Zonal Shift. You'll see traffic will stop going to the AZ you specify.
