(() => {
  const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : 'https://algosenseibackend.onrender.com';

  const STORAGE_KEY = 'algosensei_analytics';
  const TOPIC_KEYS = ['arrays', 'strings', 'linked_lists', 'trees', 'graphs', 'dp'];
  const TOPIC_LABELS = {
    arrays: 'Arrays',
    strings: 'Strings',
    linked_lists: 'Linked Lists',
    trees: 'Trees',
    graphs: 'Graphs',
    dp: 'DP',
  };

  const DOMAIN_TO_TOPICS = {
    dsa: ['arrays', 'strings', 'linked_lists', 'trees', 'graphs', 'dp'],
    dbms: ['strings'],
    oop: ['strings'],
    os: ['trees', 'graphs'],
    system_design: ['graphs', 'trees'],
  };

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function readAnalytics() {
    const fallback = {
      questionsSolved: 0,
      codeReviewsCompleted: 0,
      interviewsCompleted: 0,
      topicCounts: TOPIC_KEYS.reduce((acc, key) => ({ ...acc, [key]: 0 }), {}),
      reviewScores: [],
      interviewScores: [],
      completedModes: [],
      lastUpdated: null,
    };

    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (!stored) {
        return fallback;
      }
      return {
        ...fallback,
        ...stored,
        topicCounts: { ...fallback.topicCounts, ...(stored.topicCounts || {}) },
        reviewScores: Array.isArray(stored.reviewScores) ? stored.reviewScores : [],
        interviewScores: Array.isArray(stored.interviewScores) ? stored.interviewScores : [],
        completedModes: Array.isArray(stored.completedModes) ? stored.completedModes : [],
      };
    } catch (error) {
      return fallback;
    }
  }

  function saveAnalytics(data) {
    const nextData = {
      ...data,
      lastUpdated: new Date().toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextData));
    return nextData;
  }

  function recordTopicPractice(topic, weight = 1) {
    const normalized = String(topic || 'mixed').toLowerCase();
    const analytics = readAnalytics();
    if (normalized === 'mixed') {
      saveAnalytics(analytics);
      return;
    }
    if (DOMAIN_TO_TOPICS[normalized]) {
      DOMAIN_TO_TOPICS[normalized].forEach((mappedTopic) => {
        analytics.topicCounts[mappedTopic] = (analytics.topicCounts[mappedTopic] || 0) + weight;
      });
    } else if (TOPIC_KEYS.includes(normalized)) {
      analytics.topicCounts[normalized] += weight;
    }
    saveAnalytics(analytics);
  }

  function recordQuestionSolved(topic = 'mixed') {
    const analytics = readAnalytics();
    analytics.questionsSolved += 1;
    analytics.completedModes.push({ mode: 'mentor', topic, timestamp: new Date().toISOString() });
    saveAnalytics(analytics);
    recordTopicPractice(topic, 1);
  }

  function recordCodeReview(topic = 'mixed', score = null) {
    const analytics = readAnalytics();
    analytics.codeReviewsCompleted += 1;
    analytics.completedModes.push({ mode: 'code_review', topic, score, timestamp: new Date().toISOString() });
    if (typeof score === 'number') {
      analytics.reviewScores.push(score);
    }
    saveAnalytics(analytics);
    recordTopicPractice(topic, 1);
  }

  function recordInterviewCompleted(domain = 'dsa', score = null) {
    const analytics = readAnalytics();
    analytics.interviewsCompleted += 1;
    analytics.completedModes.push({ mode: 'mock_interview', topic: domain, score, timestamp: new Date().toISOString() });
    if (typeof score === 'number') {
      analytics.interviewScores.push(score);
    }
    saveAnalytics(analytics);
    recordTopicPractice(domain, 2);
  }

  function calculateReadinessScore(analytics) {
    const topicCoverage = TOPIC_KEYS.filter((key) => (analytics.topicCounts[key] || 0) > 0).length;
    const activityScore = analytics.questionsSolved * 8 + analytics.codeReviewsCompleted * 10 + analytics.interviewsCompleted * 15;
    const balanceScore = topicCoverage * 5;
    const interviewAverage = analytics.interviewScores.length
      ? analytics.interviewScores.reduce((sum, score) => sum + score, 0) / analytics.interviewScores.length
      : 50;
    const reviewAverage = analytics.reviewScores.length
      ? analytics.reviewScores.reduce((sum, score) => sum + score, 0) / analytics.reviewScores.length
      : 50;

    return clamp(Math.round((activityScore + balanceScore + interviewAverage * 0.3 + reviewAverage * 0.2)), 0, 100);
  }

  function getTopicStats(analytics) {
    return TOPIC_KEYS.map((key) => {
      const value = analytics.topicCounts[key] || 0;
      return {
        key,
        label: TOPIC_LABELS[key],
        value,
        progress: clamp(value * 18, 0, 100),
      };
    });
  }

  function getWeakAreas(analytics) {
    return getTopicStats(analytics)
      .filter((topic) => topic.value <= 1)
      .map((topic) => topic.label)
      .slice(0, 3);
  }

  function getStrongAreas(analytics) {
    return getTopicStats(analytics)
      .filter((topic) => topic.value >= 3)
      .map((topic) => topic.label)
      .slice(0, 3);
  }

  function getDashboardModel() {
    const analytics = readAnalytics();
    return {
      analytics,
      readinessScore: calculateReadinessScore(analytics),
      weakAreas: getWeakAreas(analytics),
      strongAreas: getStrongAreas(analytics),
      topics: getTopicStats(analytics),
    };
  }

  function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');

    const applyTheme = (theme) => {
      const isDark = theme === 'dark';
      document.documentElement.classList.toggle('dark', isDark);
      if (sunIcon && moonIcon) {
        sunIcon.classList.toggle('hidden', isDark);
        moonIcon.classList.toggle('hidden', !isDark);
      }
    };

    const preferredTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(preferredTheme);

    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        const nextTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
        localStorage.setItem('theme', nextTheme);
        applyTheme(nextTheme);
      });
    }
  }

  function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const header = document.querySelector('header');

    if (!mobileMenuBtn || !mobileMenu) {
      return;
    }

    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      if (header) {
        mobileMenu.style.top = `${header.offsetHeight}px`;
      }
    });
  }

  window.AlgoSensei = {
    BACKEND_URL,
    TOPIC_KEYS,
    TOPIC_LABELS,
    DOMAIN_TO_TOPICS,
    clamp,
    initThemeToggle,
    initMobileMenu,
    readAnalytics,
    saveAnalytics,
    recordTopicPractice,
    recordQuestionSolved,
    recordCodeReview,
    recordInterviewCompleted,
    calculateReadinessScore,
    getDashboardModel,
  };
})();