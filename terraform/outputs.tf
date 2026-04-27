output "rds_endpoint" {
  description = "RDS connection endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "rds_db_name" {
  description = "RDS database name"
  value       = aws_db_instance.postgres.db_name
}

output "beanstalk_env_cname" {
  description = "Elastic Beanstalk Environment CNAME/URL"
  value       = aws_elastic_beanstalk_environment.env.cname
}

output "codebuild_project_name" {
  description = "Name of the CodeBuild project (Build stage of the pipeline)"
  value       = aws_codebuild_project.ci.name
}

output "ci_artifacts_bucket" {
  description = "S3 bucket that stores CI artifacts (source + build output)"
  value       = aws_s3_bucket.ci_artifacts.bucket
}

output "codepipeline_name" {
  description = "Name of the CodePipeline that listens to commits on master"
  value       = aws_codepipeline.ci.name
}

output "github_connection_arn" {
  description = "ARN of the CodeStar GitHub connection (must be authorized manually in the AWS console before the first pipeline run)"
  value       = aws_codestarconnections_connection.github.arn
}
