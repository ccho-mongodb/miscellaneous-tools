gem 'octokit'
require 'octokit'
require 'csv'

# TODO: update authentication as PAT is no longer a valid way to auth.

# How to run:
# 1. Setup a GitHub personal access token (PAT)
# 2. Add key value in GITHUB_PERSONAL_APP_KEY environment value
# 3. Execute with `ruby sankey.rb`

# Reports on GitHub-related metrics that we care about for our Engineering Team OKRs
# for the current quarter.

GITHUB_ACCESS_TOKEN = ENV['GITHUB_PERSONAL_APP_KEY']
REPO = '10gen/apidocs'
REPORT_CSV = 'sankey.arrays'

def export_to_csv(fn, cols, data)
  CSV.open(fn, 'w' ) do |csv|
    csv << cols
    data.each do |row|
      csv << cols.map { |key| row[key] }
    end
  end
end

def year_start(now = Time.now)
  Time.new(now.year, 5, 1)
end

def quarter_start(now = Time.now)
  start_t = nil

  case now.month
  when 1
    start_t = Time.new(now.year-1, 11, 1)
  when 2..4
    start_t = Time.new(now.year, 2, 1)
  when 5..7
    start_t = Time.new(now.year, 5, 1)
  when 8..10
    start_t = Time.new(now.year, 8, 1)
  when 11..12
    start_t = Time.new(now.year, 11, 1)
  end

  return start_t
end

# all closed PRs from specific date
def qualified_pull_requests(client, repo, from_t, **opts)

  prs = []
  page = 1 # 1-based index
  per_page = opts[:per_page] || 100
  has_more = true

  while has_more
    # assumption: created_at sorted in descending order
    pull_requests = client.pull_requests(repo, { per_page: per_page, state: "closed", page: page })
    break if pull_requests == nil

    prs_qualified_by_time = pull_requests.select {|pr| pr.created_at >= from_t}
    prs += prs_qualified_by_time

    # At least one of the PRs did not meet if false
    has_more = false if pull_requests.count != prs_qualified_by_time.count

    page += 1
  end

  prs
end

def review_stats(client, repo, issue_no, author)
  reviews = client.pull_request_reviews(repo, issue_no)
  return {} if reviews.nil?

  # ignore author's review
  reviews.select {|r| r[:user][:login] != author}.sort_by{|r| r[:created_at]}.map{|r| r[:user][:login]}
rescue Octokit::NotFound => nfe
  p "#{nfe.backtrace.join("\n\t")}"
  {}
end

def time_elapsed(from_t, to_t)
  return nil if from_t.nil? || to_t.nil?
  ((to_t - from_t) / 60).ceil
end

def build_key(author, reviewer)
  "#{author}:#{reviewer}"
end

### main
skipped = [] # PRs that lack "review me" label or review requested and have been merged
@data = []

client = Octokit::Client.new(:access_token => GITHUB_ACCESS_TOKEN)
#start_time = Time.new(2020, 7, 1)
#start_time = Time.now
#t = quarter_start(start_time)
# t = year_start(start_time)
t = Time.new(2020, 7, 1)
p "#{Time.now}: Starting run for all PRs since #{t}"

@reviewer_data = {}

prs = qualified_pull_requests(client, REPO, t)
prs.each do |pr|
  begin
    item = {
      pull_request_id: pr.id,
      issue_no: pr.number,
      created_at: pr.created_at,
      author: pr.user.login,
      merged_at: pr.merged_at
    }

    reviewers = review_stats(client, REPO, item[:issue_no], item[:author])

    reviewers.each do |reviewer|
      key = build_key(pr.user.login, reviewer)

      if @reviewer_data.key? key
        @reviewer_data[key] += 1
      else
        @reviewer_data[key] = 1
      end
    end
  rescue StandardError => e
    puts "Pull request #{item[:issue_no]} not qualified. #{e.backtrace.join("\n\t")}"
  end
end

#reformat @reviewer_data
@reviewer_data.each do |k,v|
  a,b = k.split(':')
  p "[ '#{a}', '#{b}-reviewer', #{v} ],"
end
