output "ecr_repository_url" {
  description = "ECR repository URL for pushing images"
  value       = aws_ecr_repository.windtrend.repository_url
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = length(aws_lambda_function.windtrend) > 0 ? aws_lambda_function.windtrend[0].function_name : "not deployed yet"
}

output "github_actions_role_arn" {
  description = "Add this to GitHub Secrets as AWS_ROLE_ARN"
  value       = aws_iam_role.github_actions.arn
}
