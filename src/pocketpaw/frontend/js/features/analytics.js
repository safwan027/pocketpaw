/**
 * PocketPaw - Analytics and Trace Explorer Feature Module
 *
 * Created: 2026-04-20
 *
 * Integrates dashboard UI with:
 * - /api/v1/analytics/*
 * - /api/v1/traces
 * - /api/v1/traces/{trace_id}
 */

window.PocketPaw = window.PocketPaw || {};

window.PocketPaw.Analytics = {
    name: 'Analytics',

    getState() {
        return {
            showAnalyticsModal: false,
            analyticsTab: 'overview', // overview | traces
            analyticsPeriod: 'day',   // day | week | month
            analyticsLoading: false,
            analyticsError: '',

            analyticsCost: null,
            analyticsPerformance: null,
            analyticsUsage: null,
            analyticsHealth: null,

            tracesLoading: false,
            tracesError: '',
            traces: [],
            traceSince: '',
            traceSessionFilter: '',
            traceMinCost: 0,
            traceLimit: 50,

            selectedTraceId: '',
            selectedTrace: null,
            selectedTraceLoading: false,
            selectedTraceError: '',

            _analyticsPollTimer: null,
        };
    },

    getMethods() {
        return {
            openAnalytics() {
                this.showAnalyticsModal = true;
                this.analyticsError = '';
                this.tracesError = '';
                this.selectedTraceError = '';
                this.refreshAnalyticsPanel();
                this._startAnalyticsPoll();
                this.$nextTick(() => {
                    if (window.refreshIcons) window.refreshIcons();
                });
            },

            closeAnalyticsPanel() {
                this.showAnalyticsModal = false;
                this._stopAnalyticsPoll();
            },

            setAnalyticsTab(tab) {
                this.analyticsTab = tab;
                if (tab === 'traces' && (!Array.isArray(this.traces) || this.traces.length === 0)) {
                    this.refreshTraces();
                }
            },

            setAnalyticsPeriod(period) {
                if (this.analyticsPeriod === period) return;
                this.analyticsPeriod = period;
                this.refreshAnalyticsData();
            },

            async refreshAnalyticsPanel() {
                await Promise.all([this.refreshAnalyticsData(), this.refreshTraces()]);
            },

            async _fetchAnalyticsJson(url) {
                const resp = await fetch(url);
                let data = null;
                try {
                    data = await resp.json();
                } catch (_) {
                    data = null;
                }

                if (!resp.ok) {
                    const detail = data && (data.detail || data.error);
                    throw new Error(detail || `Request failed (${resp.status})`);
                }
                return data;
            },

            async refreshAnalyticsData() {
                this.analyticsLoading = true;
                this.analyticsError = '';

                try {
                    const period = encodeURIComponent(this.analyticsPeriod || 'day');
                    const [cost, performance, usage, health] = await Promise.all([
                        this._fetchAnalyticsJson(`/api/v1/analytics/cost?period=${period}`),
                        this._fetchAnalyticsJson(`/api/v1/analytics/performance?period=${period}`),
                        this._fetchAnalyticsJson(`/api/v1/analytics/usage?period=${period}`),
                        this._fetchAnalyticsJson('/api/v1/analytics/health'),
                    ]);

                    this.analyticsCost = cost;
                    this.analyticsPerformance = performance;
                    this.analyticsUsage = usage;
                    this.analyticsHealth = health;
                } catch (err) {
                    this.analyticsError = err && err.message ? err.message : 'Failed to load analytics';
                } finally {
                    this.analyticsLoading = false;
                }
            },

            async refreshTraces() {
                this.tracesLoading = true;
                this.tracesError = '';

                try {
                    const params = new URLSearchParams();
                    if (this.traceSince && this.traceSince.trim()) {
                        params.set('since', this.traceSince.trim());
                    }
                    if (this.traceSessionFilter && this.traceSessionFilter.trim()) {
                        params.set('session_id', this.traceSessionFilter.trim());
                    }
                    params.set('min_cost', String(Math.max(0, Number(this.traceMinCost) || 0)));
                    params.set('limit', String(Math.max(1, Number(this.traceLimit) || 50)));

                    const traces = await this._fetchAnalyticsJson(`/api/v1/traces?${params.toString()}`);
                    this.traces = Array.isArray(traces) ? traces : [];

                    if (!this.selectedTraceId && this.traces.length > 0) {
                        await this.selectTrace(this.traces[0].trace_id);
                    } else if (this.selectedTraceId) {
                        const found = this.traces.some(t => t.trace_id === this.selectedTraceId);
                        if (found) {
                            await this.selectTrace(this.selectedTraceId);
                        } else {
                            this.selectedTraceId = '';
                            this.selectedTrace = null;
                        }
                    }
                } catch (err) {
                    this.tracesError = err && err.message ? err.message : 'Failed to load traces';
                } finally {
                    this.tracesLoading = false;
                }
            },

            clearTraceFilters() {
                this.traceSince = '';
                this.traceSessionFilter = '';
                this.traceMinCost = 0;
                this.traceLimit = 50;
                this.refreshTraces();
            },

            async selectTrace(traceId) {
                if (!traceId) return;

                this.selectedTraceId = traceId;
                this.selectedTraceLoading = true;
                this.selectedTraceError = '';

                try {
                    this.selectedTrace = await this._fetchAnalyticsJson(
                        `/api/v1/traces/${encodeURIComponent(traceId)}`
                    );
                } catch (err) {
                    this.selectedTrace = null;
                    this.selectedTraceError =
                        err && err.message ? err.message : 'Failed to load trace detail';
                } finally {
                    this.selectedTraceLoading = false;
                }
            },

            _startAnalyticsPoll() {
                this._stopAnalyticsPoll();
                this._analyticsPollTimer = setInterval(() => {
                    if (!this.showAnalyticsModal) {
                        this._stopAnalyticsPoll();
                        return;
                    }

                    this.refreshAnalyticsData();
                    if (this.analyticsTab === 'traces') {
                        this.refreshTraces();
                    }
                }, 30000);
            },

            _stopAnalyticsPoll() {
                if (this._analyticsPollTimer) {
                    clearInterval(this._analyticsPollTimer);
                    this._analyticsPollTimer = null;
                }
            },

            analyticsCostTotals() {
                return (this.analyticsCost && this.analyticsCost.totals) || {};
            },

            analyticsLatencyStats() {
                return (this.analyticsPerformance && this.analyticsPerformance.response_latency_ms) || {};
            },

            analyticsUsageTotals() {
                return (this.analyticsUsage && this.analyticsUsage.totals) || {};
            },

            analyticsTopModels(limit = 6) {
                const rows = this.analyticsCost && Array.isArray(this.analyticsCost.by_model)
                    ? this.analyticsCost.by_model
                    : [];
                return rows.slice(0, limit);
            },

            analyticsTopChannels(limit = 6) {
                const rows = this.analyticsUsage && Array.isArray(this.analyticsUsage.messages_by_channel)
                    ? this.analyticsUsage.messages_by_channel
                    : [];
                return rows.slice(0, limit);
            },

            analyticsTopTools(limit = 8) {
                const rows = this.analyticsPerformance && Array.isArray(this.analyticsPerformance.tool_performance)
                    ? this.analyticsPerformance.tool_performance
                    : [];
                return rows.slice(0, limit);
            },

            analyticsFmtCurrency(value) {
                const n = Number(value);
                if (!Number.isFinite(n)) return '$0.00';

                if (Math.abs(n) >= 1) {
                    return `$${n.toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                    })}`;
                }

                return `$${n.toLocaleString(undefined, {
                    minimumFractionDigits: 4,
                    maximumFractionDigits: 4,
                })}`;
            },

            analyticsFmtNumber(value) {
                const n = Number(value);
                if (!Number.isFinite(n)) return '0';
                return n.toLocaleString();
            },

            analyticsFmtPercent(value, assumeFraction = true) {
                const n = Number(value);
                if (!Number.isFinite(n)) return '0%';
                const normalized = assumeFraction ? n * 100 : n;
                return `${normalized.toFixed(2)}%`;
            },

            analyticsFmtMs(value) {
                const n = Number(value);
                if (!Number.isFinite(n)) return '0 ms';
                return `${n.toFixed(1)} ms`;
            },

            analyticsFmtBytes(value) {
                const n = Number(value);
                if (!Number.isFinite(n) || n <= 0) return '0 B';

                const units = ['B', 'KB', 'MB', 'GB', 'TB'];
                let size = n;
                let unitIndex = 0;
                while (size >= 1024 && unitIndex < units.length - 1) {
                    size /= 1024;
                    unitIndex += 1;
                }
                return `${size.toFixed(unitIndex === 0 ? 0 : 2)} ${units[unitIndex]}`;
            },

            analyticsFmtWhen(value) {
                if (!value) return '-';
                const d = new Date(value);
                if (Number.isNaN(d.getTime())) return String(value);
                return d.toLocaleString();
            },

            analyticsShort(value, maxLength = 42) {
                const text = String(value || '');
                if (!text) return '';
                if (text.length <= maxLength) return text;
                return `${text.slice(0, maxLength - 3)}...`;
            },

            analyticsStatusClass(status) {
                const normalized = String(status || '').toLowerCase();
                if (normalized === 'ok' || normalized === 'healthy') {
                    return 'bg-success/20 text-success border border-success/30';
                }
                if (normalized === 'warning' || normalized === 'degraded') {
                    return 'bg-warning/20 text-warning border border-warning/30';
                }
                if (normalized === 'error' || normalized === 'unhealthy' || normalized === 'critical') {
                    return 'bg-danger/20 text-danger border border-danger/30';
                }
                if (normalized === 'command') {
                    return 'bg-accent/20 text-accent border border-accent/30';
                }
                return 'bg-white/10 text-white/60 border border-white/15';
            },

            analyticsTraceErrorSummary(trace) {
                if (!trace || !Array.isArray(trace.errors) || trace.errors.length === 0) return '';
                const first = trace.errors[0] || {};
                const message = first.message || 'Trace has errors';
                return this.analyticsShort(message, 120);
            },
        };
    },
};

if (window.PocketPaw.Loader) {
    window.PocketPaw.Loader.register('Analytics', window.PocketPaw.Analytics);
}
