-- Heritage Parlor — Initial Database Schema
-- Reference file for Lovable.app / Supabase setup
-- Run this in the Supabase SQL Editor to create all tables

-- ═══════════════════════════════════════════
-- PROFILES
-- ═══════════════════════════════════════════

CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  display_name TEXT NOT NULL,
  avatar_url TEXT,
  bio TEXT,
  favorite_categories TEXT[] DEFAULT '{}',
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  is_admin BOOLEAN DEFAULT FALSE,
  contribution_count INT DEFAULT 0,
  games_logged INT DEFAULT 0
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT USING (true);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE USING (auth.uid() = id);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, display_name)
  VALUES (new.id, COALESCE(new.raw_user_meta_data->>'display_name', split_part(new.email, '@', 1)));
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ═══════════════════════════════════════════
-- GAME LOG
-- ═══════════════════════════════════════════

CREATE TABLE game_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  game_id TEXT NOT NULL,
  played_at TIMESTAMPTZ DEFAULT NOW(),
  rating INT CHECK (rating BETWEEN 1 AND 5),
  notes TEXT,
  player_count INT,
  duration_minutes INT,
  would_play_again BOOLEAN
);

CREATE INDEX idx_game_log_user ON game_log(user_id);
CREATE INDEX idx_game_log_game ON game_log(game_id);

ALTER TABLE game_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own game log"
  ON game_log FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own game log"
  ON game_log FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own game log"
  ON game_log FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own game log"
  ON game_log FOR DELETE USING (auth.uid() = user_id);

-- Update games_logged count on insert
CREATE OR REPLACE FUNCTION update_games_logged()
RETURNS trigger AS $$
BEGIN
  UPDATE profiles SET games_logged = (
    SELECT COUNT(*) FROM game_log WHERE user_id = NEW.user_id
  ) WHERE id = NEW.user_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_game_logged
  AFTER INSERT OR DELETE ON game_log
  FOR EACH ROW EXECUTE FUNCTION update_games_logged();

-- ═══════════════════════════════════════════
-- COMMUNITY RATINGS
-- ═══════════════════════════════════════════

CREATE TABLE community_ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id TEXT NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  vote INT CHECK (vote IN (-1, 1)),
  tip TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(game_id, user_id)
);

CREATE INDEX idx_ratings_game ON community_ratings(game_id);

ALTER TABLE community_ratings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view ratings"
  ON community_ratings FOR SELECT USING (true);

CREATE POLICY "Users can insert own ratings"
  ON community_ratings FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own ratings"
  ON community_ratings FOR UPDATE USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════
-- FAVORITES
-- ═══════════════════════════════════════════

CREATE TABLE favorites (
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  game_id TEXT NOT NULL,
  added_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, game_id)
);

ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own favorites"
  ON favorites FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own favorites"
  ON favorites FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own favorites"
  ON favorites FOR DELETE USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════
-- SEASONAL CHALLENGES
-- ═══════════════════════════════════════════

CREATE TABLE seasonal_challenges (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  theme TEXT NOT NULL,
  game_ids TEXT[] NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  badge_name TEXT,
  badge_svg TEXT,
  is_active BOOLEAN DEFAULT TRUE
);

ALTER TABLE seasonal_challenges ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view challenges"
  ON seasonal_challenges FOR SELECT USING (true);

CREATE POLICY "Admins can manage challenges"
  ON seasonal_challenges FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = true)
  );

-- ═══════════════════════════════════════════
-- CHALLENGE PROGRESS
-- ═══════════════════════════════════════════

CREATE TABLE challenge_progress (
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  challenge_id UUID REFERENCES seasonal_challenges(id) ON DELETE CASCADE,
  game_id TEXT NOT NULL,
  completed_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, challenge_id, game_id)
);

ALTER TABLE challenge_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own progress"
  ON challenge_progress FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
  ON challenge_progress FOR INSERT WITH CHECK (auth.uid() = user_id);

-- ═══════════════════════════════════════════
-- GAME SUGGESTIONS
-- ═══════════════════════════════════════════

CREATE TABLE game_suggestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id TEXT NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  suggestion_text TEXT NOT NULL,
  suggestion_type TEXT CHECK (suggestion_type IN ('tip', 'variant', 'correction', 'house_rule')),
  upvotes INT DEFAULT 0,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE game_suggestions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view approved suggestions"
  ON game_suggestions FOR SELECT USING (status = 'approved' OR auth.uid() = user_id);

CREATE POLICY "Users can insert suggestions"
  ON game_suggestions FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Admins can manage suggestions"
  ON game_suggestions FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = true)
  );

-- ═══════════════════════════════════════════
-- SUBMITTED GAMES
-- ═══════════════════════════════════════════

CREATE TABLE submitted_games (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  source TEXT,
  category TEXT,
  player_count TEXT,
  equipment TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'published')),
  admin_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE submitted_games ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own submissions"
  ON submitted_games FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert submissions"
  ON submitted_games FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Admins can manage submissions"
  ON submitted_games FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = true)
  );

-- ═══════════════════════════════════════════
-- COMMISSIONS
-- ═══════════════════════════════════════════

CREATE TABLE commissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id TEXT NOT NULL,
  user_id UUID REFERENCES profiles(id),
  customer_name TEXT NOT NULL,
  customer_email TEXT NOT NULL,
  customization_notes TEXT,
  stripe_checkout_id TEXT,
  stripe_payment_intent TEXT,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'in_progress', 'shipped', 'completed', 'cancelled')),
  amount_cents INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE commissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own commissions"
  ON commissions FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can manage commissions"
  ON commissions FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = true)
  );

-- ═══════════════════════════════════════════
-- LULU ORDERS
-- ═══════════════════════════════════════════

CREATE TABLE lulu_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES profiles(id),
  kit_type TEXT NOT NULL,
  game_ids TEXT[] NOT NULL,
  lulu_print_job_id TEXT,
  status TEXT DEFAULT 'pending',
  tracking_url TEXT,
  amount_cents INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE lulu_orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own orders"
  ON lulu_orders FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can manage orders"
  ON lulu_orders FOR ALL USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND is_admin = true)
  );

-- ═══════════════════════════════════════════
-- GAME NIGHT EVENTS
-- ═══════════════════════════════════════════

CREATE TABLE game_night_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  host_user_id UUID REFERENCES profiles(id),
  title TEXT NOT NULL,
  description TEXT,
  theme TEXT,
  game_ids TEXT[] NOT NULL,
  event_date TIMESTAMPTZ,
  location_type TEXT CHECK (location_type IN ('in_person', 'virtual', 'hybrid')),
  max_attendees INT,
  is_public BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE game_night_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view public events"
  ON game_night_events FOR SELECT USING (is_public = true OR auth.uid() = host_user_id);

CREATE POLICY "Users can create events"
  ON game_night_events FOR INSERT WITH CHECK (auth.uid() = host_user_id);

CREATE POLICY "Hosts can update own events"
  ON game_night_events FOR UPDATE USING (auth.uid() = host_user_id);

CREATE POLICY "Hosts can delete own events"
  ON game_night_events FOR DELETE USING (auth.uid() = host_user_id);

-- ═══════════════════════════════════════════
-- EVENT RSVPS
-- ═══════════════════════════════════════════

CREATE TABLE event_rsvps (
  event_id UUID REFERENCES game_night_events(id) ON DELETE CASCADE,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'going' CHECK (status IN ('going', 'maybe', 'declined')),
  PRIMARY KEY (event_id, user_id)
);

ALTER TABLE event_rsvps ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view RSVPs for public events"
  ON event_rsvps FOR SELECT USING (true);

CREATE POLICY "Users can manage own RSVPs"
  ON event_rsvps FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own RSVPs"
  ON event_rsvps FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own RSVPs"
  ON event_rsvps FOR DELETE USING (auth.uid() = user_id);
