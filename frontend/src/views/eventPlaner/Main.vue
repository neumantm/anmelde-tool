<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!loading">
            <v-card-title class="text-center justify-center my-6">
              Diese Fahrten kannst du bearbeiten
            </v-card-title>
            <v-card-actions class="justify-center align-center">
              <v-btn x-large color="success" @click="onNewClicked">
                <v-icon left>mdi-calendar-plus</v-icon>
                Neue Fahrt erstellen
              </v-btn>
            </v-card-actions>
            <v-expansion-panels class="mt-3">
              <v-expansion-panel v-for="(item, index) in items" :key="index">
                <v-expansion-panel-header>
                  <v-list-item :key="item.name">
                    <v-list-item-avatar>
                      <v-icon :class="'primary'" dark>
                        mdi-tent
                      </v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ item.name }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        {{ item.description }}
                      </v-list-item-subtitle>

                      <v-list-item-subtitle>
                        {{ getLagerText(item) }}
                      </v-list-item-subtitle>

                      <v-list-item-subtitle>
                        {{ getDeadline(item) }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card flat max-width="500" class="mx-auto">
                    <v-list>
                      <v-list-item>
                        <v-btn
                          class="ma-2"
                          color="info"
                          @click="editCompleteEvent(item.id)"
                        >
                        <v-icon left> mdi-pencil </v-icon>
                          Bearbeite das ganze Event
                        </v-btn>
                        <v-btn
                          class="ma-2"
                          color="error"
                          @click="deleteEvent(item.id)"
                        >
                        <v-icon left> mdi-trash-can </v-icon>
                          Event löschen
                        </v-btn>
                      </v-list-item>
                    <template v-for="(stepName, editIndex) in steps">
                      <v-list-item :key="editIndex + 1">
                        <v-list-item-content>
                          {{ stepName }}
                        </v-list-item-content>
                        <v-list-item-action>
                          <v-btn
                            @click="editEvent(editIndex + 1, item.id)"
                            icon
                            color="secondary"
                          >
                            <v-icon dark color="primary"> mdi-pencil</v-icon>
                          </v-btn>
                        </v-list-item-action>
                      </v-list-item>
                        <v-divider :key="`divider ${editIndex + 1}`"></v-divider>
                    </template>
                    </v-list>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
          <v-card v-else>
            <div class="text-center ma-5">
              <p>Lade Daten ...</p>
              <v-progress-circular
                :size="80"
                :width="10"
                class="ma-5"
                color="primary"
                indeterminate
              ></v-progress-circular>
              <p>Bitte hab etwas Geduld.</p>
            </div>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
    <PreEventCreation
      ref="preEventCreationRef"
      @createEvent="onCreateEvent"
    />
    <EventDeleteModal
      ref="eventDeleteModalRef"
      @refresh="refresh"
    />
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import PreEventCreation from '@/components/dialog/PreEventCreation.vue';
import EventDeleteModal from '@/components/dialog/EventDeleteModal.vue';

export default {
  name: 'EventPlanerMain',
  mixins: [apiCallsMixin],
  components: {
    PreEventCreation,
    EventDeleteModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    loading: true,
    steps: [
      'Aktionsbeschreibung',
      'Stammdaten',
      'Verifizierungscode',
      'Daten und Uhrzeit',
      'Ort',
      'Teilnehmer_innen Beitrag',
      'Autorisierung',
      'Registrierungsmodel',
      'Sichtbarkeit',
      'Registrierungübersicht',
    ],
  }),
  computed: {},
  methods: {
    getLagerText(item) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);
      return `Termin: ${moment(startDate, 'll', 'de').format('ll')} bis
      ${moment(endDate, 'll', 'de').format('ll')}`;
    },
    getDeadline(item) {
      const registrationDeadline = new Date(item.registrationDeadline);
      return `Anmeldeschluss: ${moment(registrationDeadline, 'll', 'de').format(
        'll',
      )}`;
    },
    onNewClicked() {
      this.$refs.preEventCreationRef.open();
    },
    deleteEvent(id) {
      this.$refs.eventDeleteModalRef.open(id);
    },
    onCreateEvent(data) {
      this.createNewEvent(data);
    },
    createNewEvent(data) {
      axios
        .post(`${this.API_URL}/event/event/`, {
          eventPlanerModules: [data.authName, data.bookingOption],
          name: data.name,
          personalDataRequired: data.personalDataRequired,
        })
        .then((success) => {
          const newEventId = success.data.id;
          this.$router.push({
            name: 'planEvent',
            params: { id: newEventId },
          });
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim erstellen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
        });
    },
    editEvent(step, eventId) {
      this.$router.push({
        name: 'planEvent',
        params: {
          step,
          id: eventId,
        },
      });
    },
    editCompleteEvent(eventId) {
      this.$router.push({
        name: 'planEvent',
        params: {
          id: eventId,
        },
      });
    },
    refresh() {
      this.getEventPlanerOverview()
        .then((respone) => {
          this.items = respone.data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim anzeigen der Events aufgetreten, '
              + 'bitte probiere es später nocheinmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    this.refresh();
  },
};
</script>
