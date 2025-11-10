use colored::*;

/// ASCII art cats for various occasions
pub const CAT_HAPPY: &str = r#"
    /\_/\
   ( o.o )
    > ^ <
"#;

pub const CAT_WORKING: &str = r#"
    /\_/\
   ( -.- )
    > ^ <  *typing*
"#;

pub const CAT_CELEBRATING: &str = r#"
    /\_/\
   ( ^.^ )
    > ^ <  YAY!
"#;

pub const CAT_ERROR: &str = r#"
    /\_/\
   ( x.x )
    > ^ <  *hairball*
"#;

pub const CAT_SLEEPING: &str = r#"
    /\_/\
   ( -.- ) Zzz
    > ^ <
"#;

pub const BANNER: &str = r#"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🐱 CATPARSER - The Purrfect Document Parser 🐱            ║
║                                                               ║
║   Meowvelously fast • Whisker-sharp accuracy                 ║
║   Powered by Rust 🦀 • Cat-approved ✓                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"#;

/// Cat-themed messages
pub const CAT_PUNS: &[&str] = &[
    "Paws-itively parsing your documents!",
    "Feline fine and parsing fast!",
    "Meow-velous progress!",
    "Purr-fect parsing in progress!",
    "Cat-ching all those documents!",
    "This is paws-itively amazing!",
    "Fur-ociously fast processing!",
    "Claw-ver parsing detected!",
    "Having a meow-gical time parsing!",
    "Whisker-licking good performance!",
];

/// Print the welcome banner
pub fn print_banner() {
    println!("{}", BANNER.bright_cyan().bold());
}

/// Print a cat with a message
pub fn print_cat_message(cat_art: &str, message: &str, color: Color) {
    println!("{}", cat_art.color(color));
    println!("{}", message.color(color).bold());
    println!();
}

/// Print a section header
pub fn print_section(title: &str) {
    let separator = "─".repeat(60);
    println!();
    println!("{}", separator.bright_black());
    println!("🐾 {}", title.bright_yellow().bold());
    println!("{}", separator.bright_black());
}

/// Print a key-value stat
pub fn print_stat(key: &str, value: &str, emoji: &str) {
    println!("  {} {}: {}", emoji, key.bright_white(), value.bright_green().bold());
}

/// Print a random cat pun
pub fn print_random_pun() {
    use std::time::{SystemTime, UNIX_EPOCH};
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let idx = (timestamp as usize) % CAT_PUNS.len();
    println!("{}", CAT_PUNS[idx].bright_magenta().italic());
}

/// Print progress message
pub fn print_progress(message: &str) {
    println!("  🐾 {}", message.cyan());
}

/// Print success message
pub fn print_success(message: &str) {
    println!("{}", message.bright_green().bold());
}

/// Print error message
pub fn print_error(message: &str) {
    println!("{}", message.bright_red().bold());
}

/// Print warning message
pub fn print_warning(message: &str) {
    println!("{}", message.bright_yellow().bold());
}

/// Print a fancy divider
pub fn print_divider() {
    println!("{}", "═".repeat(60).bright_black());
}

/// Print results summary with cats
pub fn print_results_summary(
    total_articles: usize,
    total_errors: usize,
    years_range: Option<(i32, i32)>,
    processing_time: f64,
) {
    print_section("📊 Purr-ocessing Results");

    print_stat("Total Articles", &total_articles.to_string(), "📚");
    print_stat("Hairballs (Errors)", &total_errors.to_string(), "🤢");

    if let Some((min_year, max_year)) = years_range {
        print_stat("Years Range", &format!("{} - {}", min_year, max_year), "📅");
    }

    print_stat("Processing Time", &format!("{:.2}s", processing_time), "⚡");
    print_stat(
        "Throughput",
        &format!("{:.0} docs/sec", total_articles as f64 / processing_time),
        "🚀",
    );

    println!();

    if total_errors == 0 {
        print_cat_message(CAT_CELEBRATING, "Paw-some! No errors detected!", Color::Green);
    } else if total_errors < total_articles / 100 {
        print_cat_message(CAT_HAPPY, "Great job! Very few hairballs!", Color::Yellow);
    } else {
        print_cat_message(CAT_ERROR, "Uh-oh, quite a few hairballs...", Color::Red);
    }
}

/// Print top N items from a sorted list
pub fn print_top_items(title: &str, items: &[(String, usize)], limit: usize) {
    print_section(title);

    for (i, (key, count)) in items.iter().take(limit).enumerate() {
        let rank = format!("#{}", i + 1);
        let bar = "█".repeat((count / items[0].1 * 30).max(1));
        println!(
            "  {} {:<10} {} {}",
            rank.bright_yellow(),
            key.bright_white(),
            bar.bright_cyan(),
            count.to_string().bright_green().bold()
        );
    }
    println!();
}
