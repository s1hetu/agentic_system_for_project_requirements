
-----------------------------------------------START: 01_project_understanding.md-----------------------------------------------------------

# Project Requirements: 

## Project Requirements
The project must deliver an AI-powered solution that leverages 15+ years of Envirol’s plant data and, where relevant, integrates external data sources to predict grease collection market trends, optimize recycling operations, and generate actionable insights through a user-friendly dashboard. The system should deliver predictive analytics for operational efficiency, compliance, and market understanding, with clear differentiation between required and secondary features. 
- Forecast which restaurants are likely to miss grease trap cleanings in the current and next month.
- Assign dynamic, data-driven grades to each establishment based on historical and predictive insights.
- Aggregate and analyze internal data with relevant external data sources (such as weather, economic trends) using structured data feeds or APIs for enhanced forecasting.
- Predict future grease collection volumes and market size.
- Optimize route planning and generate smart inspection schedules.
- Identify potential illegal dumping locations and instances.
- Analyze and explain revenue fluctuations.
- Evaluate reductions in environmental impact due to improved practices.
- Present all analyses and KPIs via a clear, interactive dashboard.

## Project Understanding
This project seeks to empower Envirol with advanced analytics that combine internal plant data and pertinent external factors to enhance forecasting, operational planning, compliance, and insight delivery. The initiative aims to streamline grease trap recycling and collection, proactively identify market shifts, and address illegal disposal challenges through data-driven automation. Comprehensive reporting and visualization will better equip management and operational teams to make strategic decisions and demonstrate environmental responsibility.
- Integrates both historical company data and external datasets for refined, multidimensional forecasting.
- Promotes operational optimization and regulatory compliance through automated predictive tools.
- Provides accessible, actionable insights for better business management and environmental stewardship.

## Project Scope
Design, build, and implement an AI analytics platform that combines Envirol’s historical plant data with relevant external data (e.g., weather, economic indicators) via structured integrations, enabling prediction of market trends, grease collection volumes, scheduling optimization, compliance risk identification, financial and environmental analysis, and dashboard-based reporting.


-----------------------------------------------END: 01_project_understanding.md-----------------------------------------------------------


-----------------------------------------------START: 02_key_objectives.md-----------------------------------------------------------

# Key Objectives: 

 ## Key Objectives

Key objectives define the essential, measurable outcomes that the AI system for Envirol's grease trap recycling operations must achieve. These objectives ensure that project success is clearly targeted and that all stakeholder priorities—predictive insights, operational optimizations, and environmental improvements—are addressed with quantifiable metrics for progress and value.

- Accurately predict 90% or more of restaurants likely to miss grease trap cleaning in the current and following month.
- Assign dynamic grades to 100% of establishments monthly, with automated updates reflecting recent cleaning and compliance data.
- Forecast future grease collection volumes for up to 12 months ahead, achieving a prediction accuracy within a ±10% error margin.
- Generate optimized collection and inspection schedules that reduce operational mileage by at least 20%.
- Identify at least 95% of anomalous grease trap dumping incidents, including illegal disposals in deserts, valleys, or trash cans.
- Provide outlet-specific pattern analysis via a dashboard accessible by stakeholders, with insights updating daily.
- Deliver analytical reports explaining revenue fluctuations within a 48-hour window, attributing >80% of anomalies to specific causes.
- Quantify and track reductions in environmental impact, aiming for a 15% increase in proper grease waste dumping within the first year.
- Develop AI-powered methods to flag a minimum of 85% of suspected non-legal cleanings for follow-up action.


-----------------------------------------------END: 02_key_objectives.md-----------------------------------------------------------


-----------------------------------------------START: 03_deliverables.md-----------------------------------------------------------

# Deliverables: 

## Project Deliverables

- AI model for market size prediction
- AI model for forecasting grease collection volumes
- Data integration of 15+ years of plant data
- Integration of external data sources for market analysis
- Predictive analytics for identifying restaurants likely to miss cleaning in the current and next month
- Establishment grading and dynamic scoring system
- Detection of patterns in outlet-specific data
- User-friendly dashboard for presenting insights and analytics
- Optimization engine for collection route and schedule planning
- Smart scheduling system for inspectors
- Predictive detection of potential illegal grease trap waste dumping locations
- Analysis and reporting of revenue fluctuations with identified causes
- Analytical assessment of environmental impact reduction from improved dumping practices
- Methods and tools to identify non-legal grease trap cleanings


-----------------------------------------------END: 03_deliverables.md-----------------------------------------------------------


---------------------------------------------START: Web Chatbot INTERFACE-----------------------------------

# Web Chatbot
An interactive chatbot accessible through the web interface to inquire about predictions, market insights, or scheduling, facilitating quick information retrieval.


## Web Chatbot

 

### User
*Actions*:
- Initiate conversations by typing questions or requests.
- Receive real-time responses from the chatbot.
- Ask follow-up questions to clarify or expand information.
- End the chat session when finished.
- Provide feedback on the chatbot's responses.
- Access suggested questions or prompts to assist conversation.


## Scheduling Assistant

 

### User
**Appointment Management**
*Actions*:
- Create new appointments by specifying date, time, and details.
- Reschedule existing appointments to different dates and times.
- Cancel scheduled appointments.
- View a list of upcoming appointments.
- Inquire about details of specific appointments.
- Receive reminders for upcoming appointments.
- Modify appointment details such as participants or notes.
- Confirm appointment attendance or decline invitations.


## Information Retrieval System

 

### User
*Actions*:
- Submit queries to search for relevant information.
- Refine search queries to improve retrieval accuracy.
- View retrieved information in an organized format.
- Bookmark or save retrieved information for future reference.
- Receive suggestions or related topics based on user queries.

----------------------------------END: Web Chatbot INTERFACE--------------------------------------





---------------------------------------------START: Mobile App INTERFACE-----------------------------------

# Mobile App
A mobile application enabling field staff and inspectors to access schedules, input data, and receive real-time notifications during operations.


## Schedule Access

 

### Field Staff
**Schedule Viewing**
*Actions*:
- View daily, weekly, and monthly schedules.
- Access details of assigned routes and locations.
- Review upcoming tasks and deadlines.
- Receive real-time updates on schedule modifications.
- Check task and route priorities.

### Inspectors
**Schedule and Task Management**
*Actions*:
- View assigned inspection routes and schedules.
- Access detailed information for upcoming inspection tasks.
- Receive alerts for schedule changes or urgent tasks.
- Review inspection deadlines and priorities.
- Confirm task completion status within scheduled times.


## Data Input

 

### Field Staff
  **Inspection Data Entry**
     *Actions*:
       - Input inspection data into designated forms.
       - Attach photos relevant to inspection points.
       - Add comments or notes for specific inspection items.
       - Fill out required fields in inspection forms.
       - Submit collected data instantly for processing and storage.


## Real-time Notifications

 

### Staff
**Notification Management**  
*Actions*:
- Receive push notifications or alerts for schedule changes, new assignments, emergencies, or important updates.  
- View notifications history and status (read/unread).  
- Acknowledge and mark notifications as read.  
- Customize notification preferences for different event types.


## Task Management

 

### Staff
**Task Handling**
*Actions*:
- View a list of assigned tasks with relevant details.
- Check off tasks upon completion.
- Update task statuses to reflect progress or delays.
- Log notes and comments related to each task.
- Edit or modify task details, including deadlines and priority.


## Offline Functionality

 

### User
**Offline Access and Data Management**
*Actions*:
- View schedules and relevant data stored locally on the device.
- Input or modify data offline within the local application.
- Save data locally for future synchronization.
- After reconnection, synchronize offline data with the central server.
- Detect internet connectivity status and notify users about sync status.
- Resolve data conflicts during synchronization through predefined rules.

----------------------------------END: Mobile App INTERFACE--------------------------------------





---------------------------------------------START: Web App INTERFACE-----------------------------------

# Web App
A comprehensive web-based dashboard providing insights, predictions, and analytics related to market trends and recycling operations.


## Market & Recycling Analytics Dashboard

 

### User
**Dashboard Viewer**  
*Actions*:
- Access the analytics dashboard to view consolidated data on market trends and recycling operations.
- Generate and customize visual reports and charts based on selected data parameters.
- Filter data by date ranges, regions, and specific recycling activities.
- Export visual reports and raw data for external analysis.
- Save preferred dashboard configurations for quick access.
- Receive alerts or notifications about significant market changes or recycling operation anomalies.

### Data Analyst
**Data Processing and Analysis**  
*Actions*:
- Import and update datasets related to market trends and recycling operations.
- Cleanse and validate collected data to ensure accuracy and consistency.
- Create and update analytical models and algorithms for trend forecasting.
- Develop visualizations such as charts, heatmaps, and dashboards.
- Generate comprehensive reports summarizing insights and findings.
- Monitor data integrity and resolve discrepancies or missing information.
- Maintain historical data archives for trend comparisons.

### System Administrator
**Platform Maintenance and Security**  
*Actions*:
- Configure user access levels and permissions for dashboard users.
- Monitor system performance and optimize data processing workflows.
- Ensure data security and compliance with privacy regulations.
- Backup system configurations and datasets regularly.
- Manage platform updates and troubleshoot issues.
- Audit user activity and access logs for security purposes.


## Market Trends Insights

 

### User
  **Analyze Market Trends**
     *Actions*:
       - Access and review visual representations of current and historical market data.
       - Identify patterns and significant changes in market behavior.
       - Generate trend reports based on analyzed data.
       - Compare different market segments over specified time periods.
       - Export trend insights and visualizations for external use.
  **Manage Insights Preferences**
     *Actions*:
       - Customize visualization types and display parameters.
       - Set preferences for data ranges and specific market segments.
       - Subscribe to updates on selected market trends.
       - Adjust notification settings for trend analysis updates.


## Recycling Operations Analytics

 

### Operations Analyst
**Performance Metrics**
*Actions*:
- Generate reports on recycling throughput and volume.
- Analyze collection and processing times for efficiency.
- Track key performance indicators (KPIs) related to recycling operations.
- Identify trends and patterns in recycling data over specified periods.

**Process Efficiencies**
*Actions*:
- Assess the duration of each recycling process stage.
- Identify bottlenecks and delays within recycling workflows.
- Compare actual process durations against benchmarks.
- Evaluate the effectiveness of process improvements implemented.

**Operational Insights**
*Actions*:
- Provide detailed insights on waste types and quantities processed.
- Visualize data on operational performance through charts and dashboards.
- Monitor resource utilization and equipment efficiency.
- Deliver actionable recommendations based on data analysis.

----------------------------------END: Web App INTERFACE--------------------------------------





---------------------------------------------START: WhatsApp Chatbot INTERFACE-----------------------------------

# WhatsApp Chatbot
A messaging-based chatbot allowing stakeholders to receive alerts, generate reports, or ask questions via WhatsApp, supporting remote communication and decision-making.


## WhatsApp Chatbot

 

### Stakeholders
*Actions*:
- Send real-time alerts and notifications to stakeholders via WhatsApp.
- Allow stakeholders to receive and view system reports through WhatsApp messages.
- Enable stakeholders to ask questions and get responses related to system data using WhatsApp.
- Facilitate stakeholders in confirming actions or approvals through WhatsApp interactions.
- Collect stakeholder inputs and feedback via WhatsApp messages to inform system adjustments.


## Alert System

 

### Stakeholder
  **Notification Delivery**
    *Actions*:
    - Send timely alerts to stakeholders through WhatsApp regarding critical events or updates.
    - Manage the list of stakeholders designated to receive notifications.
    - Schedule notifications to be sent at specific times or after certain events occur.
    - Track delivery status and confirmation of received notifications.
    - Customize the content and format of the notifications based on event type and stakeholder preferences.
    - Enable or disable specific notification types for individual stakeholders.
    - Log notification history for auditing and review purposes.


## Report Generation

 

### End User
*Actions*:
- Initiate report requests through WhatsApp chat.
- Specify report parameters or select report types within WhatsApp.
- Receive generated reports or data summaries directly in the WhatsApp chat.
- Request updated or refreshed reports when needed.
- Track status of report generation requests.
- Provide feedback or report issues regarding report delivery.

### Support Staff
*Actions*:
- Process report requests received via WhatsApp.
- Generate reports based on user-specified parameters.
- Deliver reports directly into the user’s WhatsApp chat.
- Handle requests for report updates or clarifications.
- Monitor report request logs and user feedback.
- Troubleshoot delivery issues or report errors.


## Natural Language Processing (NLP)

 

### Stakeholder
*Actions*:
- Process incoming messages from stakeholders and interpret their intent.
- Recognize and extract key entities and parameters from user inputs.
- Generate contextually appropriate responses based on interpreted queries.
- Handle natural language variations and synonyms effectively.
- Clarify ambiguous or unclear user inputs through follow-up questions.
- Map user requests to corresponding system functionalities or workflows.
- Improve understanding accuracy through learning from interactions.
- Log and store conversational data for future analysis and system tuning.

----------------------------------END: WhatsApp Chatbot INTERFACE--------------------------------------




