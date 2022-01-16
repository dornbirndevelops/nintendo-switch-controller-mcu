/*
 * Copyright (c) 2012-2014 Wind River Systems, Inc.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr.h>
#include <sys/printk.h>

#include <net/net_if.h>
#include <net/net_core.h>
#include <net/net_context.h>
#include <net/net_mgmt.h>

#include <esp_wifi.h>
#include <esp_timer.h>
#include <esp_event.h>


// #include <net/hostname.h>
// #include <net/if.h>>
// #include <net/wifi.h>
// #include <net/wifi_mgmt.h>

/* routes:
* / -> serve web frontend
* /api/connect -> connect to switch console
* /api/disconnect -> disconnect from switch console
* /api/set (payload instructions) -> load instructions into internal state, stop instruction execution if needed.
* /api/play -> start instruction execution
* /api/pause -> halts instruction execution
* /api/stop -> resets instruction execution
*/

void main(void)
{
	printk("Hello World! %s\n", CONFIG_BOARD);

	
	// connect to WIFI
	


	// obtain IP address

	// start Web Server

	// "web server available at <ip>"
}
