import json
import logging
import boto3
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

# Fixed S3 bucket name
BUCKET_NAME = 'lab-aws-workshop'

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for processing Bedrock agent requests.
    Saves customer segment analysis results to S3.
    """
    try:
        logger.info(f'Received event: {json.dumps(event, indent=2)}')
        
        action_group = event.get('actionGroup')
        function = event.get('function')
        parameters = event.get('parameters', [])
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})

        logger.info(f'Parameters: {parameters}')
        logger.info(f'Parameters length: {len(parameters)}')

        # Extract analysis_result from parameters
        analysis_data = None
        
        if parameters:
            for param in parameters:
                logger.info(f'Parameter: {param}')
                if param.get('name') == 'analysis_result':
                    analysis_data = param.get('value')
                    break
        else:
            logger.warning('No parameters found in event')

        if not analysis_data:
            logger.error('Missing analysis_result parameter')
            raise ValueError('Missing required parameter: analysis_result. Make sure to pass the analysis JSON as a string parameter.')

        logger.info(f'Received analysis_data: {analysis_data}')

        # Parse analysis_data if it's a string
        # if isinstance(analysis_data, str):
        #     try:
        #         analysis_data = json.loads(analysis_data)
        #     except json.JSONDecodeError as e:
        #         logger.error(f'Failed to parse analysis_data as JSON: {str(e)}')
        #         raise ValueError(f'Invalid JSON format in analysis_result: {str(e)}')

        logger.info(f'Parsed analysis data: {json.dumps(analysis_data, indent=2)}')

        # Generate S3 file path with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f'ai_agent_demo/customer_analysis_{timestamp}.json'

        # Wrap analysis_data in the desired structure
        data_to_save = {"data": analysis_data}

        # Save to S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data_to_save, indent=2),
            ContentType='application/json'
        )

        logger.info(f'Successfully saved analysis to s3://{BUCKET_NAME}/{s3_key}')

        # Return success response in Bedrock format
        return {
            'messageVersion': '1.0',
            'response':
            {
                'actionGroup': action_group,
                'function': function,
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': f'✓ Successfully saved customer segment analysis to S3:\ns3://{BUCKET_NAME}/{s3_key}'
                        }
                    }
                }
            },
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }

    except ValueError as e:
        logger.error(f'Validation error: {str(e)}')
        return {
            'messageVersion': '1.0',
            'response':
            {
                'actionGroup': event.get('actionGroup'),
                'function': event.get('function'),
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': f'Error: {str(e)}'
                        }
                    }
                }
            },
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}', exc_info=True)
        return {'messageVersion': '1.0',
            'response':
            {
                'actionGroup': event.get('actionGroup'),
                'function': event.get('function'),
                'functionResponse': {
                    'responseBody': {
                        'TEXT': {
                            'body': f'Error saving to S3: {str(e)}'
                        }
                    }
                }
            },
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }