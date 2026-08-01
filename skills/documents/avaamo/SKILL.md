---
name: avaamo
description: 'In case you are unable to receive the expected response from the Dialog
  skill, you can debug using the following troubleshooting tips:'
---

# Source: https://docs.avaamo.com/user-guide/how-to/build-skills/create-skill/using-dialog-designer/debug-skill.md

# Debug Dialog skill

In case you are unable to receive the expected response from the **Dialog** skill, you can debug using the following troubleshooting tips:

### **Using Insights**

* Click the eye icon below the user query to know the intent mapped to the query.

![](https://2934665269-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LpXFTiTgns4Ml77XGi3%2Fuploads%2FPxboti2ZCBfPk3fsI6Dj%2Fimage.png?alt=media\&token=68d3ace9-72b0-46f9-a2a6-4e94e8fcc980)

* In the **Insights** pop-up, you can know if the query is mapped to the required intent type, skill name, intent name, response node, and the language of the query. &#x20;

![](https://2934665269-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-LpXFTiTgns4Ml77XGi3%2Fuploads%2FHzK8Y1jqkHzcbBP2Ya1c%2Fimage.png?alt=media\&token=be325a36-93cb-49c5-98e2-5746e1b2f232)

* You can then consider updating the conversation flow, if required, based on the details available in the insights.&#x20;

### Using Debug logs

Use console.log to log messages at specific steps in the script. This helps to verify if the script is executing as expected and to identify points of failure. You can then use the **Debug logs** options in **Dialog skill** to display all the logs generated using console.log.

Consider that in the **Order skill** of the **Pizza agent**,  you have logged **context** for an intent:

```markup
console.log(context);
```

* In the **Dialog skill** page, click the **Debug  -> Debug logs** option in the left navigation menu.&#x20;
* Click the **agent** icon in the bottom-right corner.
* Enter the pizza order details. Context details are displayed in the **Debug logs** window. Similarly, you can use **console.log** to log messages at specific steps in the script, as required.

{% hint style="info" %}
**Note**: In the `Debug logs` pop-up window, a maximum of 50 consecutive `Console.log` statements can be printed.
{% endhint %}

### Using Conversation history

You can check the user query from the [Conversation history](https://docs.avaamo.com/user-guide/build-agents/debug-agents#conversation-history) to view the complete flow that caused an error or unexpected response.
